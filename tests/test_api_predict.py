from fastapi.testclient import TestClient

from solarops_api.main import app

VALID_PAYLOAD = {
    "poa_irradiance": 700.0,
    "ambient_temperature": 25.0,
    "wind_speed": 3.0,
    "hour": 12,
    "month": 6,
    "dayofyear": 166,
}


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


def test_predict_model_unavailable():
    with TestClient(app) as client:
        app.state.model = None
        response = client.post("/predict", json=VALID_PAYLOAD)
        assert response.status_code == 503