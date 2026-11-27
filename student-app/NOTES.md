# SolarOps Student Dashboard — Notes

## What I Built

A Streamlit dashboard for SolarOps that shows:

1. Date range picker.
2. Actual vs Predicted chart (filtered to daylight).
3. Trust summary (ok, anomaly, unreliable_input).
4. Top 20 anomalies table (formatted and highlighted).
5. Model card.

**Extension Chosen: Option B** (Download anomalies as CSV).

## What I Wrote Myself

- **Panel 2 (Chart):** I added the logic to filter `poa > 50` and used `st.line_chart` to plot actual and predicted values.
- **Panel 4 (Table):** I used `get_anomalies()`, added custom formatting (2 decimals), and highlighted bad rows with red color using Pandas styling.
- **Extension (CSV):** I added an `st.download_button` with a primary style and icon to export the anomaly table.

## What I Studied (and Did Not Copy)

- I looked at `app/` to understand how Streamlit charts and tables are structured.
- I wrote my own logic for filtering and displaying data.
- I did not modify `pipeline.py`, `predict.py`, `dashboard.py`, or `v3.pkl`.

## How to Run

```bash
uv run streamlit run student-app/streamlit_app.py
```
