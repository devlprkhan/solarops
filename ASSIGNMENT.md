# SolarOps — Student Assignment: Build the Dashboard

## What you're building

A Streamlit web app that uses our trained model (`models/v3.pkl`) to show
solar performance intelligence: expected vs actual power, trust labels, and
anomalies worth investigating.

**You do NOT retrain the model. You do NOT deploy. You build the app locally,
then submit it as a Pull Request for review.**

---

## Step 0 — Setup (do this first, do not skip)

```bash
# 1. Fork the repo on GitHub, then clone your fork
gh repo fork devlprkhan/solarops --clone
cd solarops

# 2. Install dependencies
uv sync
# If it hangs on "universal-data-cleaner", remove that line from pyproject.toml
# and run `uv sync` again.

# 3. Add the dataset
#    Download PVDAQ System 2107 CSVs (see README.md)
#    Place them in: data/raw/pvdaq/2023-solar-data-prize/system-2107/
```

**Step 0 verification — run this before writing any code:**

```bash
uv run jupyter lab notebooks/02_clean_pipeline.ipynb
```

Run the notebook top-to-bottom (Kernel → Restart & Run All).
**Expected final result: v1 MAE = 38.755, R² = 0.917.**

If it fails, stop and fix setup. Do not proceed until this works.

---

## Step 1 — Understand the model you're using

Read these files (in order):

1. `src/solarops/pipeline.py` — how data is loaded and aligned
2. `src/solarops/predict.py` — how to load the model and make predictions
3. `src/solarops/dashboard.py` — one-call bridge (`load_test_predictions`, `get_model_card`, `get_anomalies`, `predict_one`)
4. `models/v3_metadata.json` — model version, features, metrics
5. `notebooks/07_save_model.ipynb` — working example of loading + predicting
6. `notebooks/06_reliability_and_anomalies.ipynb` — how trust labels are computed

**Key facts:**

- Model: LightGBM v3, MAE = 25.69 kW, R² = 0.952
- Features required: `poa_irradiance_o_149574`, `ambient_temperature_o_149575`,
  `wind_speed_o_149576`, `hour`, `month`, `dayofyear`
- `predict()` **refuses rows with missing POA** — this is correct behavior.
  Handle it in your app (show a badge), don't `try/except: pass`.

---

## Step 2 — Study the reference app

Before you build, run **our** production app:

```bash
uv run streamlit run app/app.py
```

Click through all 6 pages: **Overview · Anomalies · Investigate · Predict · Model**.

**What you're looking at:**

- A working multi-page Streamlit app (`st.navigation` + `pages/` folder)
- Real plotly charts, real model predictions
- Trust labels, anomaly table, custom-input predictor

**Read the code** (it's in `app/`):

- `app/app.py` — entry point, defines page order
- `app/pages/overview.py` — actual vs predicted + heatmap
- `app/pages/anomalies.py` — top anomalies + CSV export
- `app/pages/investigate.py` — day drill-down
- `app/pages/predict.py` — custom-input prediction
- `app/pages/model.py` — model card

**Do not copy-paste.** Reviewer will diff and fail it. Use it as **study material** — learn the patterns, then write your own.

---

## Step 3 — Build your app

Create **`student-app/streamlit_app.py`** (a starter with 2 TODOs already exists — extend it).

Run locally with:

```bash
uv run streamlit run student-app/streamlit_app.py
```

### Required panels (all 5 must exist)

| #   | Panel                              | Details                                                                                                                                 |
| --- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Date range picker**              | Let user pick a start/end date from the test period                                                                                     |
| 2   | **Actual vs Predicted line chart** | Two lines: actual AC power, predicted AC power. Same axis. Filter to daylight (`poa > 50`) so the chart isn't dominated by night zeros. |
| 3   | **Trust badge counts**             | Show counts for `ok / anomaly / unreliable_input`. Reuse the logic from `notebooks/06`.                                                 |
| 4   | **Top-N anomalies table**          | 10–20 rows sorted by residual (actual − predicted). Most negative first = worst underperformance.                                       |
| 5   | **Model card**                     | Read `models/v3_metadata.json` → show version, MAE, R², trained_at.                                                                     |

The **starter already has** panels 1, 3, 5 working. Your job: fill in **panels 2 and 4**.

### Optional extension (choose ONE)

- **A.** Click anomaly row → 7-day context plot around that row
- **B.** Download anomalies as CSV button
- **C.** Month heatmap: predicted vs actual by month
- **D.** Missing-POA sensor-gap timeline (bar chart of missing rows per day)

Pick one. Do it well. Don't do all four.

---

## Step 4 — Rules (strict — auto-fail if broken)

| ✅ Do                                                   | ❌ Don't                                                               |
| ------------------------------------------------------- | ---------------------------------------------------------------------- |
| Use `pipeline.py`, `predict.py`, `dashboard.py` as-is   | Modify `pipeline.py`, `predict.py`, `dashboard.py`, or `models/v3.pkl` |
| Put your code in `student-app/`                         | Retrain the model                                                      |
| Write `student-app/NOTES.md` (what you copied vs wrote) | `try/except: pass` around `predict()`                                  |
| Handle missing POA with a badge                         | Submit without NOTES.md                                                |
| Add only new files in `student-app/`                    | Modify `app/`, `notebooks/01-07`                                       |

**Why so strict?** The pipeline is a shared contract. If your PR changes it,
other students' PRs break. Wrap what you need, don't touch the base.

**Why can't I copy from `app/`?** Because the point of the assignment is to
understand the code well enough to rebuild it differently. If your PR is a
near-identical copy, you'll be asked to explain every line in a live review.
Don't try it.

---

## Step 5 — Submit via Pull Request

1. Push your work:

   ```bash
   git checkout -b dashboard-<your-name>
   git add student-app/
   git commit -m "dashboard: <your-name> — Streamlit app"
   git push origin dashboard-<your-name>
   ```

2. Open PR to `devlprkhan/solarops:main`:
   - Title: `[student] <your-name> — dashboard`
   - Description must include:
     - Screenshot of your running app
     - Which extension you chose (A/B/C/D)
     - The command the reviewer runs: `uv run streamlit run student-app/streamlit_app.py`

3. **Do not open the PR until it runs locally without errors.**

---

## Step 6 — Grading rubric

| #   | Check                                                    | Points |
| --- | -------------------------------------------------------- | ------ |
| 1   | App launches without errors on reviewer's machine        | 15     |
| 2   | All 5 required panels render correctly                   | 25     |
| 3   | Actual vs Predicted uses real v3 predictions (not dummy) | 15     |
| 4   | Trust labels correct (unreliable_input on missing POA)   | 15     |
| 5   | Extension works as described                             | 20     |
| 6   | `NOTES.md` present + no edits to shared files            | 10     |

**Passing = 70. Excellent = 90+.**

**Auto-fail:**

- Modified `pipeline.py`, `predict.py`, `dashboard.py`, or `v3.pkl`
- Modified anything in `app/`
- `predict()` wrapped in bare `try/except`
- App doesn't launch on reviewer's machine
- No `NOTES.md`
- **Near-identical copy of `app/streamlit_app.py`** — will be caught in review

---

## Known traps (read before you get stuck)

1. **`uv sync` hangs** — remove `universal-data-cleaner` from `pyproject.toml`.
2. **`predict()` raises `ValueError: missing POA`** — correct. Show a badge, don't crash. See `notebooks/07` Cell 11.
3. **Chart is a flat line** — first test rows are night (0.42 kW). Filter to `poa > 50`.
4. **`pd.concat(axis=1)` doubles rows** — always `assert len(X) == len(y)` before model calls. See `notebooks/06` Cell 7.
5. **Streamlit doesn't reload model changes** — restart the server if `v3.pkl` changes.

---

## Timeline (4 weeks)

| Week | Deliverable                                                     | What's reviewed    |
| ---- | --------------------------------------------------------------- | ------------------ |
| 1    | PR with `NOTES.md` + note that baseline reproduced (MAE 38.755) | Setup works        |
| 2    | Local app with panels 1–3                                       | Core functionality |
| 3    | All 5 panels + extension                                        | Complete app       |
| 4    | Polished app + screenshots                                      | Final PR           |

**Weekly PR updates = weekly review.** Don't save it all for the end.

---

## Questions?

Ask in the class channel before spending more than 30 minutes stuck.
Good questions include: the exact error, what you tried, which file/line.
Bad question: "it doesn't work."

Good luck.
