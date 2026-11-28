"""SolarOps — STUDENT dashboard. Fast, professional, light/dark compatible.
Run: uv run streamlit run student-app/streamlit_app.py
"""

import streamlit as st
import pandas as pd
from solarops.dashboard import (
    load_test_predictions, get_model_card, get_anomalies, predict_one,
)

# Page setup
st.set_page_config(page_title="SolarOps", layout="wide")

# CSS for professional look
st.markdown("""
    <style>
    .stMetric { background-color: rgba(128, 128, 128, 0.1); padding: 10px; border-radius: 8px; }
    .stDataFrame { font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# --- CACHE DATA LOADING ---
@st.cache_data
def get_data():
    # Ye ek hi baar chalta hai
    return load_test_predictions()

@st.cache_data
def get_precomputed_anomalies(df):
    # Saare data ke anomalies pehle se nikaal lo taake date change pe fast ho
    return get_anomalies(df, n=10000)

df = get_data()
card = get_model_card()

st.title("☀️ SolarOps — Solar Performance Intelligence")
st.caption(f"Model **{card['version']}** · MAE **{card['metrics']['MAE']:.1f} kW** · R² **{card['metrics']['R2']:.3f}**")

# --- PANEL 1: Date Picker ---
st.sidebar.header("Filters")
start, end = st.sidebar.date_input(
    "Date range",
    value=(df["measured_on"].min().date(), df["measured_on"].max().date()),
    min_value=df["measured_on"].min().date(),
    max_value=df["measured_on"].max().date(),
)

# --- FAST FILTERING ---
# String compare ki bajaye direct datetime compare karo, ye super fast hota hai
mask = (df["measured_on"] >= pd.to_datetime(start)) & (df["measured_on"] <= pd.to_datetime(end) + pd.Timedelta(days=1))
view = df[mask]

# --- PANEL 2: Chart ---
st.subheader("📈 Actual vs Predicted AC Power")
# Filter daylight
daylight = view[view["poa"] > 50].set_index("measured_on")[["actual", "predicted"]]
if len(daylight) == 0:
    st.warning("No daylight data in selected range (poa > 50).")
else:
    st.line_chart(daylight, color=["#1f77b4", "#ff7f0e"])

# --- PANEL 3: Trust Badges ---
st.subheader("🛡️ Trust Summary")
c1, c2, c3 = st.columns(3)
c1.metric("✅ OK", f"{(view['trust'] == 'ok').sum():,}")
c2.metric("⚠️ Anomaly", f"{(view['trust'] == 'anomaly').sum():,}")
c3.metric("❌ Unreliable Input", f"{(view['trust'] == 'unreliable_input').sum():,}")

# --- PANEL 4: Anomalies Table ---
st.subheader("🚨 Top Anomalies (Worst Underperformance)")

# Precomputed anomalies ko use karo
all_anoms = get_precomputed_anomalies(df)

# Sirf current view wale anomalies chuno
anoms = all_anoms[all_anoms['measured_on'].isin(view['measured_on'])].head(20)

def highlight_anomalies(row):
    if row['actual'] == 0 or row['residual'] < -400:
        return ['background-color: #ffe6e6; color: #cc0000; font-weight: bold'] * len(row)
    return [''] * len(row)

if len(anoms) == 0:
    st.info("No anomalies in selected range.")
else:
    display_cols = ["measured_on", "actual", "predicted", "residual", "trust"]
    anoms_display = anoms[display_cols].copy()
    
    st.dataframe(
        anoms_display.style.apply(highlight_anomalies, axis=1).format(precision=2),
        use_container_width=True,
        hide_index=True,
    )
    
    # Download CSV Button
    st.download_button(
        label="📥 Download anomalies as CSV",
        data=anoms.to_csv(index=False).encode("utf-8"),
        file_name="solarops_anomalies.csv",
        mime="text/csv",
        type="primary"
    )

# --- PANEL 5: Model Card ---
with st.expander("📋 Model Card"):
    st.json(card)
    