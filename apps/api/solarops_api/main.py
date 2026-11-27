"""FastAPI application entry point for SolarOps."""

from __future__ import annotations

import logging
import math
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from solarops.predict import load_model

from .routes import router

logger = logging.getLogger("solarops_api")
logging.basicConfig(level=logging.INFO)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = PROJECT_ROOT / "models" / "v3.pkl"


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        model, metadata = load_model(MODEL_PATH)
        app.state.model = model
        app.state.metadata = metadata
        logger.info("Loaded model %s from %s", metadata.get("version"), MODEL_PATH)
    except Exception:  # noqa: BLE001
        logger.exception("Failed to load model from %s", MODEL_PATH)
        app.state.model = None
        app.state.metadata = {}
    yield
    app.state.model = None
    app.state.metadata = {}


app = FastAPI(
    title="SolarOps API",
    description="Solar power prediction service for SolarOps.",
    version="0.1.0",
    lifespan=lifespan,
)


def _sanitize_validation_value(value):
    """Recursively replace non-finite floats with None for JSON serialization."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: _sanitize_validation_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_validation_value(item) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_validation_value(item) for item in value]
    return value


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        error = dict(error)
        if "input" in error:
            error["input"] = _sanitize_validation_value(error["input"])
        errors.append(error)
    return JSONResponse(status_code=422, content={"detail": errors})


app.include_router(router)