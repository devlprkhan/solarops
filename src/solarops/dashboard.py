"""One-call bridge from pipeline → student dashboard. Students do not edit this."""

from pathlib import Path
import json
import pandas as pd

from solarops.pipeline import (
    load_raw, align_15m, split_time, impute_features,
    add_time_features, IRRADIANCE_COL,
)
from solarops.predict import load_model, predict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data/raw/pvdaq/2023-solar-data-prize/system-2107"
MODELS_DIR = PROJECT_ROOT / "models"
TIME_FEATURES = ["hour", "month", "dayofyear"]


def _trust(poa_missing, hour, residual):
    if poa_missing and 6 <= hour <= 20:
        return "unreliable_input"
    if abs(residual) >= 200:
        return "anomaly"
    return "ok"


def load_test_predictions(split_date="2022-07-01"):
    model, meta = load_model(MODELS_DIR / "v3.pkl")
    raw = load_raw(DATA_DIR)
    df = align_15m(raw)
    train, test = split_time(df, split_date)
    test = test.copy()
    test["poa_was_missing"] = test[IRRADIANCE_COL].isna()

    X_train, X_test, y_train, y_test = impute_features(train, test)
    test_fe = add_time_features(test)
    X_test_full = pd.concat([X_test, test_fe[TIME_FEATURES]], axis=1)

    preds = predict(X_test_full, model, meta["features"],
                    reject_missing_poa=False).values

    out = pd.DataFrame({
        "measured_on": test["measured_on"].values,
        "poa":         test[IRRADIANCE_COL].values,
        "actual":      y_test,
        "predicted":   preds,
        "hour":        test["measured_on"].dt.hour.values,
    })
    out["residual"] = out["actual"] - out["predicted"]
    out["trust"] = [
        _trust(m, h, r)
        for m, h, r in zip(test["poa_was_missing"].values, out["hour"], out["residual"])
    ]
    return out.sort_values("measured_on").reset_index(drop=True)


def get_model_card():
    return json.loads((MODELS_DIR / "v3_metadata.json").read_text())


def get_anomalies(df, n=20):
    out = df[df["trust"] != "unreliable_input"].copy()
    out["abs_residual"] = out["residual"].abs()
    return (out.nlargest(n, "abs_residual")
               .drop(columns="abs_residual")
               .sort_values("residual")
               .reset_index(drop=True))

def predict_one(poa, temp, wind, hour, month, dayofyear):
    """Predict one row. Returns (prediction_kW, metadata)."""
    model, meta = load_model(MODELS_DIR / "v3.pkl")
    row = pd.DataFrame([{
        "poa_irradiance_o_149574":       poa,
        "ambient_temperature_o_149575":  temp,
        "wind_speed_o_149576":           wind,
        "hour":       hour,
        "month":      month,
        "dayofyear":  dayofyear,
    }])
    pred = predict(row, model, meta["features"]).iloc[0]
    return float(pred), meta