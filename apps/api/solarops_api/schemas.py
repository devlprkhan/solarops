"""Pydantic request/response schemas for the SolarOps API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str | None = None


class ModelInfoResponse(BaseModel):
    version: str | None = None
    features: list[str] = Field(default_factory=list)
    target: str | None = None
    split_date: str | None = None
    train_range: list[str] | None = None
    test_range: list[str] | None = None
    metrics: dict[str, float] = Field(default_factory=dict)
    trained_at: str | None = None
    data: str | None = None


class PredictRequest(BaseModel):
    poa_irradiance: float = Field(..., ge=0, allow_inf_nan=False, description="Plane-of-array irradiance (W/m²)")
    ambient_temperature: float = Field(..., ge=-50, le=60, allow_inf_nan=False, description="Ambient temperature (°C)")
    wind_speed: float = Field(..., ge=0, le=40, allow_inf_nan=False, description="Wind speed (m/s)")
    hour: int = Field(..., ge=0, le=23, description="Hour of day")
    month: int = Field(..., ge=1, le=12, description="Month of year")
    dayofyear: int = Field(..., ge=1, le=366, description="Day of year")


class PredictResponse(BaseModel):
    predicted_ac_power: float
    unit: str = "kW"
    model_version: str | None = None