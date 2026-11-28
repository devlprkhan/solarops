"""API routes for SolarOps."""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd
from fastapi import APIRouter, HTTPException, Request, status

from solarops.predict import predict

from .schemas import HealthResponse, ModelInfoResponse, PredictRequest, PredictResponse

logger = logging.getLogger("solarops_api")

router = APIRouter()

FEATURE_MAP = {
    "poa_irradiance": "poa_irradiance_o_149574",
    "ambient_temperature": "ambient_temperature_o_149575",
    "wind_speed": "wind_speed_o_149576",
    "hour": "hour",
    "month": "month",
    "dayofyear": "dayofyear",
}


def _model_state(request: Request) -> tuple[Any, dict[str, Any]]:
    model = getattr(request.app.state, "model", None)
    metadata = getattr(request.app.state, "metadata", None) or {}
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded.",
        )
    return model, metadata


@router.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    model = getattr(request.app.state, "model", None)
    metadata = getattr(request.app.state, "metadata", None) or {}
    return HealthResponse(
        status="ok" if model is not None else "degraded",
        model_loaded=model is not None,
        model_version=metadata.get("version"),
    )


@router.get("/model/info", response_model=ModelInfoResponse)
def model_info(request: Request) -> ModelInfoResponse:
    _model_state(request)
    metadata = request.app.state.metadata or {}
    return ModelInfoResponse(
        version=metadata.get("version"),
        features=metadata.get("features", []),
        target=metadata.get("target"),
        split_date=metadata.get("split_date"),
        train_range=metadata.get("train_range"),
        test_range=metadata.get("test_range"),
        metrics=metadata.get("metrics", {}),
        trained_at=metadata.get("trained_at"),
        data=metadata.get("data"),
    )


@router.post("/predict", response_model=PredictResponse)
def predict_endpoint(request: Request, payload: PredictRequest) -> PredictResponse:
    model, metadata = _model_state(request)
    features = metadata.get("features")
    if not features:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model metadata is unavailable.",
        )

    row = {
        FEATURE_MAP["poa_irradiance"]: payload.poa_irradiance,
        FEATURE_MAP["ambient_temperature"]: payload.ambient_temperature,
        FEATURE_MAP["wind_speed"]: payload.wind_speed,
        FEATURE_MAP["hour"]: payload.hour,
        FEATURE_MAP["month"]: payload.month,
        FEATURE_MAP["dayofyear"]: payload.dayofyear,
    }
    df = pd.DataFrame([row])

    try:
        preds = predict(df, model, features, reject_missing_poa=True)
    except ValueError as exc:
        logger.warning("Prediction validation error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Prediction failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction failed.",
        ) from exc

    return PredictResponse(
        predicted_ac_power=float(preds.iloc[0]),
        model_version=metadata.get("version"),
    )