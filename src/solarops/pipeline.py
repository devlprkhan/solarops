"""SolarOps data pipeline: load → align → split → impute → evaluate."""

from pathlib import Path
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# column name - one place, use everywhere
IRRADIANCE_COL = "poa_irradiance_o_149574"
TEMPERATURE_COL = "ambient_temperature_o_149575"
WIND_SPEED_COL  = "wind_speed_o_149576"
TARGET_COL      = "meter_revenue_grade_ac_output_meter_149578"
FEATURES = [IRRADIANCE_COL, TEMPERATURE_COL, WIND_SPEED_COL]

def load_raw(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Load meter, environment, irradiance CSVs. Parse measured_on as datetime."""
    files = {
        "meter":       data_dir / "2107_meter_15m_data.csv",
        "environment": data_dir / "2107_environment_data.csv",
        "irradiance":  data_dir / "2107_irradiance_data.csv",
    }
    out = {}
    for name, path in files.items():
        if not path.is_file():
            raise FileNotFoundError(f"Missing {name} file: {path}")
        out[name] = pd.read_csv(path, parse_dates=["measured_on"])
    return out

def align_15m(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Filter to common window, resample irradiance to 15min, merge, sort."""
    # 1. common window across sources
    common_start = max(df["measured_on"].min() for df in raw.values())
    common_end   = min(df["measured_on"].max() for df in raw.values())

    # 2. meter target, filtered to window
    meter = raw["meter"].loc[
        raw["meter"]["measured_on"].between(common_start, common_end, inclusive="both"),
        ["measured_on", TARGET_COL],
    ].copy()

    # 3. environment features
    env = raw["environment"][["measured_on", TEMPERATURE_COL, WIND_SPEED_COL]].copy()

    # 4. irradiance resample 5min → 15min
    irr = (
        raw["irradiance"][["measured_on", IRRADIANCE_COL]]
        .sort_values("measured_on")
        .set_index("measured_on")
        .resample("15min", label="right", closed="right")
        .mean()
        .reset_index()
    )

    # 5. merge + sort
    return (
        meter
        .merge(env, on="measured_on", how="left", validate="one_to_one")
        .merge(irr, on="measured_on", how="left", validate="one_to_one")
        .sort_values("measured_on")
        .reset_index(drop=True)
    )

def split_time(df: pd.DataFrame, split_date: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Chronological split: train < split_date <= test."""
    cutoff = pd.Timestamp(split_date)
    train = df[df["measured_on"] <  cutoff].copy()
    test  = df[df["measured_on"] >= cutoff].copy()
    return train, test


def impute_features(train: pd.DataFrame, test: pd.DataFrame):
    """Fit median imputer on train[FEATURES], apply to both. Return X_train, X_test, y_train, y_test."""
    imputer = SimpleImputer(strategy="median").fit(train[FEATURES])

    X_train = pd.DataFrame(imputer.transform(train[FEATURES]), columns=FEATURES, index=train.index)
    X_test  = pd.DataFrame(imputer.transform(test[FEATURES]),  columns=FEATURES, index=test.index)

    y_train = train[TARGET_COL].values
    y_test  = test[TARGET_COL].values

    return X_train, X_test, y_train, y_test


def evaluate(model, X, y, name: str) -> dict:
    """Return {'model': name, 'MAE': ..., 'RMSE': ..., 'R2': ...}."""
    pred = model.predict(X)
    return {
        "model": name,
        "MAE":  mean_absolute_error(y, pred),
        "RMSE": mean_squared_error(y, pred) ** 0.5,
        "R2":   r2_score(y, pred),
    }

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add hour, month, dayofyear from measured_on. Returns a copy."""
    out = df.copy()
    out["hour"]      = out["measured_on"].dt.hour
    out["month"]     = out["measured_on"].dt.month
    out["dayofyear"] = out["measured_on"].dt.dayofyear
    return out