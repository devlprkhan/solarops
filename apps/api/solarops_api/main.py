"""FastAPI application entry point for SolarOps."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

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

app.include_router(router)