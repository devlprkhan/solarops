"""SolarOps — main app entry point."""

import streamlit as st

from solarops.ui import inject_styles, render_sidebar_brand, render_footer

st.set_page_config(page_title="SolarOps", page_icon="☀️", layout="wide")

inject_styles()
render_sidebar_brand()

pg = st.navigation(
    [
        st.Page("pages/overview.py", title="Overview", default=True, icon="📊"),
        st.Page("pages/anomalies.py", title="Anomalies", icon="🚨"),
        st.Page("pages/investigate.py", title="Investigate", icon="🔍"),
        st.Page("pages/predict.py", title="Predict", icon="🔮"),
        st.Page("pages/model.py", title="Model", icon="⚙️"),
    ],
    position="top",
)
pg.run()

render_footer()