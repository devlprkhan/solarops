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

# ---- Panel 2: Actual vs Predicted  ← TODO ----
st.subheader("Actual vs Predicted")
st.info("TODO: view[view['poa'] > 50].set_index('measured_on')[['actual','predicted']] → st.line_chart")

# ---- Panel 3: Trust badges (done) ----
st.subheader("Trust summary")
c1, c2, c3 = st.columns(3)
c1.metric("ok", f"{(view['trust'] == 'ok').sum():,}")
c2.metric("anomaly", f"{(view['trust'] == 'anomaly').sum():,}")
c3.metric("unreliable_input", f"{(view['trust'] == 'unreliable_input').sum():,}")

# ---- Panel 4: Anomalies table  ← TODO ----
st.subheader("Top anomalies")
st.info("TODO: st.dataframe(get_anomalies(view, n=20))")

# ---- Panel 5: Model card (done) ----
with st.expander("Model card"):
    st.json(card)