# SolarOps

Solar performance intelligence — predict expected AC power from weather + irradiance and flag underperformance.

## Why

Solar power output depends on irradiance, temperature, wind, and system condition, so raw production numbers alone cannot tell you whether a system is performing as expected. SolarOps learns the relationship between operating conditions and AC power, then compares expected versus actual output to surface meaningful deviations.

## Current status

| Stage | Focus | Status |
| --- | --- | --- |
| 1 | Data understanding + baseline | ✅ Complete |
| 2 | ML development | ✅ Complete — v3 LightGBM |
| 3 | Prediction + performance analysis | ✅ Complete — saved model + trust labels |
| 4 | Production-ready ML system | ✅ Complete — FastAPI backend + tests |
| 5 | Application + user experience | 🚧 In progress — Streamlit MVP + API integration |

## Results

Chronological split at `2022-07-01`; test period `2022-07-01` → `2023-10-31`.

| Model | Features | MAE (kW) | RMSE (kW) | R² |
| --- | --- | ---: | ---: | ---: |
| v0 — dummy (mean) | — | 196.2 | 231.6 | -0.002 |
| v1 — linear regression | 3 weather | 38.8 | 66.6 | 0.917 |
| v2 — LightGBM | 3 weather | 32.8 | 61.9 | 0.929 |
| v3 — LightGBM + time | 6 features | **25.7** | **50.8** | **0.952** |
| v4 — LightGBM + missing flags | 9 features | 25.7 | 51.0 | 0.951 |

**v3 is the production model.** It is saved as `models/v3.pkl` with `models/v3_metadata.json`. v4 added missing-value flags but did not improve MAE; ambiguous missing irradiance is handled with trust labels instead of silent imputation.

## Model

- **Algorithm:** LightGBM regressor (300 estimators, learning rate 0.05, `random_state=42`).
- **Features:** POA irradiance, ambient temperature, wind speed, hour, month, day of year.
- **Target:** meter revenue-grade AC output.
- **Artifact:** `models/v3.pkl` + versioned metadata (features, split, metrics, train/test ranges).
- **Safety:** `predict()` refuses rows with missing POA by default; pass `reject_missing_poa=False` only after handling missing input upstream.

## What it does

- Predicts expected AC power from current weather and irradiance.
- Compares expected vs actual output and computes `residual = actual - predicted`.
- Labels each prediction:
  - `ok` — features present and `|residual| < 200 kW`.
  - `anomaly` — features present and `|residual| ≥ 200 kW`.
  - `unreliable_input` — POA was missing during daylight (06:00–20:00).
- Provides a 5-page Streamlit website in `apps/dashboard/` plus a FastAPI backend in `apps/api/`:
  - **Overview** — actual vs predicted daylight chart and residual heatmap.
  - **Anomalies** — top residuals with CSV export.
  - **Investigate** — day-level drill-down with POA overlay.
  - **Predict** — custom-input prediction and daily curve.
  - **Model** — model card and residual distribution.

## Quickstart

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/devlprkhan/solarops.git
cd solarops
uv sync
```

Download the PVDAQ System 2107 CSVs and place them under:

```text
data/raw/pvdaq/2023-solar-data-prize/system-2107/
├── 2107_meter_15m_data.csv
├── 2107_environment_data.csv
└── 2107_irradiance_data.csv
```

Run the pipeline notebook and launch the applications:

```bash
uv run jupyter lab notebooks/02_clean_pipeline.ipynb
uv run uvicorn solarops_api.main:app --app-dir apps/api --reload
uv run streamlit run apps/dashboard/app.py
```

Or start both together:

```bash
uv run python scripts/dev.py
```

## Project layout

```text
src/solarops/               # shared ML and domain package
apps/api/solarops_api/      # FastAPI backend
apps/dashboard/             # Streamlit frontend
models/                     # v3.pkl + metadata
tests/                      # automated tests
notebooks/                  # 01–07: exploration → model → reliability → save
scripts/                    # data audit utilities
data/                       # local datasets (git-ignored)
```

## API endpoints

- `GET /health` — API and model status
- `GET /model/info` — model metadata
- `POST /predict` — predict expected AC power

Example request:

```json
{
  "poa_irradiance": 700.0,
  "ambient_temperature": 25.0,
  "wind_speed": 3.0,
  "hour": 12,
  "month": 6,
  "dayofyear": 166
}
```

Example response:

```json
{
  "predicted_ac_power": 285.4,
  "unit": "kW",
  "model_version": "v3"
}
```

Swagger UI: http://127.0.0.1:8000/docs

## Environment configuration

`API_BASE_URL` (default `http://127.0.0.1:8000`) configures dashboard-to-backend communication.

## Testing

```bash
uv run pytest
```

## Notebooks

| Notebook | Purpose |
| --- | --- |
| `01_initial_data_exploration` | Raw data audit and first look |
| `02_clean_pipeline` | Load, align, split, impute, v0/v1 baseline |
| `03_diagnostics` | Residual analysis of v1 |
| `04_features_and_gbm` | Time features + v2/v3 LightGBM |
| `05_worst_residuals` | Investigate v3's biggest misses |
| `06_reliability_and_anomalies` | v4 missing flags + trust labels |
| `07_save_model` | Save v3 artifact + prediction API |

## Data

The project uses **PVDAQ System 2107** from the 2023 Solar Data Prize. The data is **not included** in this repository. Download the raw CSV files from the PVDAQ dataset and place them in `data/raw/pvdaq/2023-solar-data-prize/system-2107/` as shown above. All data directories and tabular files are git-ignored.

## Roadmap / TODO

- Testing and pre-commit hooks are intentionally deferred until the pipeline and model surface stabilise.
- Completed: FastAPI prediction endpoint, dashboard API integration, and backend tests.
- Next: hyperparameter tuning, better handling of missing irradiance, CI, and deployment.

## License

MIT © 2026 devlprkhan

For architecture, roadmap, and the full project vision, see [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md).
