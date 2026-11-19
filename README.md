# SolarOps

Solar performance intelligence — predict expected AC power from weather + irradiance and flag underperformance.

## Why

Solar power output depends on irradiance, temperature, wind, and system condition, so raw production numbers alone cannot tell you whether a system is performing as expected. SolarOps learns the relationship between operating conditions and AC power, then compares expected versus actual output to surface meaningful deviations.

## Current status

| Stage | Focus | Status |
| --- | --- | --- |
| 1 | Data understanding + baseline | ✅ Complete |
| 2 | ML development | 🚧 In progress |
| 3 | Prediction + performance analysis | 📋 Planned |
| 4 | Production-ready ML system | 📋 Planned |
| 5 | Application + user experience | 📋 Planned |

Stage 1 baseline results: v0 MAE **196.2 kW**, v1 MAE **38.8 kW**, R² **0.917**.

## Quickstart

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Download the PVDAQ System 2107 CSVs and place them under:

```text
data/raw/pvdaq/2023-solar-data-prize/system-2107/
├── 2107_meter_15m_data.csv
├── 2107_environment_data.csv
└── 2107_irradiance_data.csv
```

Then run the cleaning pipeline notebook and the tests:

```bash
uv run jupyter lab notebooks/02_clean_pipeline.ipynb
uv run pytest tests/ -v
```

## Project layout

```text
src/solarops/pipeline.py   # load → align → split → impute → evaluate
notebooks/                 # exploration, cleaning pipeline, diagnostics
tests/                     # smoke tests for data pipeline + baseline model
scripts/                   # data audit utilities
data/                      # local datasets (git-ignored)
```

## Data

The project uses **PVDAQ System 2107** from the 2023 Solar Data Prize. The data is **not included** in this repository. Download the raw CSV files from the PVDAQ dataset and place them in `data/raw/pvdaq/2023-solar-data-prize/system-2107/` as shown above. All data directories and tabular files are git-ignored.

## Baseline results

| Model | MAE (kW) | RMSE (kW) | R² |
| --- | ---: | ---: | ---: |
| v0 — dummy (mean) | 196.2 | — | — |
| v1 — linear regression | 38.8 | — | 0.917 |

Chronological split at `2022-07-01`: train on earlier data, test on later data.

## License

MIT © 2026 devlprkhan

For architecture, roadmap, and the full project vision, see [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md).
