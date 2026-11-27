"""Load a saved model and produce predictions safely."""

import json
from functools import lru_cache
from pathlib import Path
import joblib
import pandas as pd

IRRADIANCE_COL = "poa_irradiance_o_149574"


@lru_cache(maxsize=4)
def load_model(path: str | Path) -> tuple:
    """Load model + metadata. Returns (model, metadata_dict)."""
    path = Path(path)
    model = joblib.load(path)
    meta_path = path.with_name(path.stem + "_metadata.json")
    metadata = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    return model, metadata


def predict(
    df: pd.DataFrame,
    model,
    feature_columns: list,
    reject_missing_poa: bool = True,
) -> pd.Series:
    """Predict on df. df must contain all feature_columns.

    By default refuses rows where POA irradiance is NaN — silently imputing
    in production produces confident wrong numbers. Caller must handle
    missing input upstream (or set reject_missing_poa=False knowingly).
    """
    missing = set(feature_columns) - set(df.columns)
    if missing:
        raise ValueError(f"df is missing features: {missing}")

    if reject_missing_poa and IRRADIANCE_COL in df.columns:
        n_missing = int(df[IRRADIANCE_COL].isna().sum())
        if n_missing:
            raise ValueError(
                f"{n_missing} row(s) have missing POA irradiance. "
                "Handle missing input upstream, or pass reject_missing_poa=False."
            )

    preds = model.predict(df[feature_columns])
    return pd.Series(preds, index=df.index, name="predicted")