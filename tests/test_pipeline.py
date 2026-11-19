"""Smoke tests for the SolarOps baseline pipeline.

These tests require the PVDAQ System 2107 raw CSVs and are skipped when the
dataset is not present locally.
"""

from pathlib import Path

import pytest
from sklearn.linear_model import LinearRegression

from solarops.pipeline import (
    align_15m,
    evaluate,
    impute_features,
    load_raw,
    split_time,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data/raw/pvdaq/2023-solar-data-prize/system-2107"

requires_data = pytest.mark.skipif(
    not DATA_DIR.is_dir(),
    reason=f"PVDAQ System 2107 data not found at {DATA_DIR}",
)


@requires_data
def test_align_shape():
    raw = load_raw(DATA_DIR)
    df = align_15m(raw)

    assert df.shape == (207140, 5)
    assert df["measured_on"].is_monotonic_increasing


@requires_data
def test_v1_beats_baseline():
    raw = load_raw(DATA_DIR)
    df = align_15m(raw)
    train, test = split_time(df, "2022-07-01")
    X_train, X_test, y_train, y_test = impute_features(train, test)

    model = LinearRegression().fit(X_train, y_train)
    metrics = evaluate(model, X_test, y_test, "v1 linear regression")

    assert metrics["MAE"] < 50
    assert metrics["R2"] > 0.85
