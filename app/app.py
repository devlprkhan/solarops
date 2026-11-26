"""SolarOps — main app entry point."""

import streamlit as st
from solarops.dashboard import load_test_predictions, get_model_card

st.set_page_config(page_title="SolarOps", layout="wide")

@st.cache_data
def _load():
    return load_test_predictions()

df = _load()
card = get_model_card()

pg = st.navigation([
    st.Page("pages/overview.py",    title="Overview",    default=True),
    st.Page("pages/anomalies.py",   title="Anomalies"),
    st.Page("pages/investigate.py", title="Investigate"),
    st.Page("pages/predict.py",     title="Predict"),
    st.Page("pages/model.py",       title="Model"),
])
pg.run()