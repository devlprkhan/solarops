"""SolarOps — STUDENT starter. Build your dashboard here.
Run: uv run streamlit run student-app/streamlit_app.py
Look at ../app/ for reference (do not copy-paste).
"""

import streamlit as st
from solarops.dashboard import (
    load_test_predictions, get_model_card, get_anomalies, predict_one,
)

st.set_page_config(page_title="SolarOps", layout="wide")

@st.cache_data
def get_data():
    return load_test_predictions()

df = get_data()
card = get_model_card()

st.title("SolarOps — Solar Performance Intelligence")
st.caption(f"model {card['version']} · MAE {card['metrics']['MAE']:.1f} kW · "
           f"R² {card['metrics']['R2']:.3f}")

# ---- Date picker (done) ----
st.sidebar.header("Filters")
start, end = st.sidebar.date_input(
    "Date range",
    value=(df["measured_on"].min().date(), df["measured_on"].max().date()),
    min_value=df["measured_on"].min().date(),
    max_value=df["measured_on"].max().date(),
)
view = df[(df["measured_on"].dt.date >= start) & (df["measured_on"].dt.date <= end)]

# ---- Panel 2: Actual vs Predicted ----
st.subheader("Actual vs Predicted")
daylight = view[view["poa"] > 50].set_index("measured_on")[["actual", "predicted"]]
if len(daylight) == 0:
    st.warning("No daylight data in selected range (poa > 50).")
else:
    st.line_chart(daylight, color=["#1f77b4", "#ff7f0e"])

# ---- Panel 3: Trust badges (done) ----
st.subheader("Trust summary")
c1, c2, c3 = st.columns(3)
c1.metric("ok", f"{(view['trust'] == 'ok').sum():,}")
c2.metric("anomaly", f"{(view['trust'] == 'anomaly').sum():,}")
c3.metric("unreliable_input", f"{(view['trust'] == 'unreliable_input').sum():,}")

# ---- Panel 4: Anomalies table ----
st.subheader("Top anomalies")

def highlight_anomalies(row):
    # Numbers ko check karna (text banane se pehle)
    if row['actual'] == 0 or row['residual'] < -400:
        return ['background-color: #ffe6e6; color: #cc0000; font-weight: bold'] * len(row)
    return [''] * len(row)

anoms = get_anomalies(view, n=20)
if len(anoms) == 0:
    st.info("No anomalies in selected range.")
else:
    display_cols = ["measured_on", "actual", "predicted", "residual", "trust"]
    anoms_display = anoms[display_cols].copy()
    
    # Colored table dikhana (Streamlit style) - Asli numbers ke sath check karein
    st.dataframe(
        anoms_display.style.apply(highlight_anomalies, axis=1).format(precision=2),
        use_container_width=True,
        hide_index=True,
    )
    
    # ---- Extension: Download anomalies as CSV ----
    st.download_button(
        label="📥 Download anomalies as CSV",
        data=anoms.to_csv(index=False).encode("utf-8"),
        file_name="solarops_anomalies.csv",
        mime="text/csv",
        help="Click to download the top anomalies as a CSV file.",
        type="primary"
    )

# ---- Panel 5: Model card (done) ----
with st.expander("Model card"):
    st.json(card)