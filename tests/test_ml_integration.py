import math

import pandas as pd
from fastapi.testclient import TestClient

from solarops.dashboard import predict_one
from solarops.predict import load_model, predict
from solarops_api.main import app

MODEL_PATH = "models/v3.pkl"
VALID_PAYLOAD = {
    "poa_irradiance": 700.0,
    "ambient_temperature": 25.0,
    "wind_speed": 3.0,
    "hour": 12,
    "month": 6,
    "dayofyear": 166,
}


def test_model_loads():
    model, metadata = load_model(MODEL_PATH)
    assert model is not None
    assert metadata["version"] == "v3"
    assert len(metadata["features"]) == 6


def test_feature_ordering():
    model, metadata = load_model(MODEL_PATH)
    features = metadata["features"]
    row = {
        "poa_irradiance_o_149574": 700.0,
        "ambient_temperature_o_149575": 25.0,
        "wind_speed_o_149576": 3.0,
        "hour": 12,
        "month": 6,
        "dayofyear": 166,
    }
    df_ordered = pd.DataFrame([row])[features]
    df_shuffled = pd.DataFrame([row])[list(reversed(features))]
    p1 = predict(df_ordered, model, features).iloc[0]
    p2 = predict(df_shuffled, model, features).iloc[0]
    assert math.isclose(p1, p2, rel_tol=1e-9)


def test_predict_one_returns_float():
    pred, meta = predict_one(700, 25, 3, 12, 6, 166)
    assert isinstance(pred, float)
    assert pred > 0


def test_consistency_direct_vs_api():
    direct_pred, _ = predict_one(700, 25, 3, 12, 6, 166)
    with TestClient(app) as client:
        response = client.post("/predict", json=VALID_PAYLOAD)
        assert response.status_code == 200
        api_pred = response.json()["predicted_ac_power"]
    assert math.isclose(direct_pred, api_pred, rel_tol=1e-6)


def test_model_load_failure():
    try:
        load_model("models/does_not_exist.pkl")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("Expected FileNotFoundError for missing artifact")