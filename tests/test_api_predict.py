import json
import math

import pytest
from fastapi.testclient import TestClient

from solarops_api.main import _sanitize_validation_value, app

VALID_PAYLOAD = {
    "poa_irradiance": 700.0,
    "ambient_temperature": 25.0,
    "wind_speed": 3.0,
    "hour": 12,
    "month": 6,
    "dayofyear": 166,
}


def _post(client, payload):
    return client.post(
        "/predict",
        content=json.dumps(payload, allow_nan=True),
        headers={"Content-Type": "application/json"},
    )


def test_predict_success():
    with TestClient(app) as client:
        response = client.post("/predict", json=VALID_PAYLOAD)
        assert response.status_code == 200
        data = response.json()
        assert "predicted_ac_power" in data
        assert data["unit"] == "kW"
        assert data["model_version"] == "v3"
        assert data["predicted_ac_power"] > 0


def test_predict_missing_field():
    with TestClient(app) as client:
        payload = dict(VALID_PAYLOAD)
        payload.pop("poa_irradiance")
        response = client.post("/predict", json=payload)
        assert response.status_code == 422


def test_predict_invalid_values():
    with TestClient(app) as client:
        payload = dict(VALID_PAYLOAD, hour=25)
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
        detail = response.json()["detail"][0]
        assert detail["loc"] == ["body", "hour"]
        assert "ctx" in detail
        assert detail["ctx"] == {"le": 23}


def test_predict_model_unavailable():
    with TestClient(app) as client:
        app.state.model = None
        response = client.post("/predict", json=VALID_PAYLOAD)
        assert response.status_code == 503


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_predict_rejects_non_finite_poa(value):
    with TestClient(app) as client:
        payload = dict(VALID_PAYLOAD, poa_irradiance=value)
        response = _post(client, payload)
        assert response.status_code == 422


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_predict_rejects_non_finite_temperature(value):
    with TestClient(app) as client:
        payload = dict(VALID_PAYLOAD, ambient_temperature=value)
        response = _post(client, payload)
        assert response.status_code == 422


def test_sanitize_validation_value_nested():
    value = {
        "numbers": [1.0, float("nan"), float("inf"), float("-inf")],
        "nested": {"x": float("nan")},
    }
    sanitized = _sanitize_validation_value(value)
    assert sanitized == {"numbers": [1.0, None, None, None], "nested": {"x": None}}


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_predict_rejects_non_finite_wind(value):
    with TestClient(app) as client:
        payload = dict(VALID_PAYLOAD, wind_speed=value)
        response = _post(client, payload)
        assert response.status_code == 422