import streamlit as st
import plotly.express as px

from solarops.dashboard import load_test_predictions, get_model_card
from solarops.ui import inject_styles, page_header, style_figure

st.set_page_config(page_title="Model", page_icon="⚙️", layout="wide")
inject_styles()
page_header("Model", "What is powering SolarOps and how it performs on held-out data.")

@st.cache_data
def _load():
    return load_test_predictions()

df = _load()
card = get_model_card()

# ---- Identity ----
st.subheader("Model identity")
id_cols = st.columns(3)
id_cols[0].metric("Version", str(card.get("version", "—")))
id_cols[1].metric("Algorithm", str(card.get("algorithm", "LightGBM")))
id_cols[2].metric("Features", str(len(card.get("features", []))))

features = card.get("features", [])
if features:
    st.caption("Features: " + ", ".join(features))

# ---- Evaluation metrics ----
metrics = card.get("metrics", {}) or card.get("test_metrics", {}) or {}
st.subheader("Evaluation metrics (held-out test period)")
if metrics:
    mcols = st.columns(len(metrics))
    for i, (k, v) in enumerate(metrics.items()):
        try:
            mcols[i].metric(k, f"{v:.3f}" if isinstance(v, float) else str(v))
        except Exception:
            mcols[i].metric(k, str(v))
else:
    st.info("No evaluation metrics found in model metadata.")

# ---- Details ----
with st.expander("Model metadata"):
    st.json(card)

# ---- Residual distribution ----
st.subheader("Residual distribution")
fig = px.histogram(df, x="residual", nbins=80)
style_figure(fig, title="Residual (kW) on test period", height=380)
st.plotly_chart(fig, use_container_width=True)

# ---- Trust mix ----
st.subheader("Prediction trust mix (test period)")
tcols = st.columns(3)
tcols[0].metric("Normal", f"{(df['trust']=='ok').sum():,}")
tcols[1].metric("Anomaly", f"{(df['trust']=='anomaly').sum():,}")
tcols[2].metric("Unreliable input", f"{(df['trust']=='unreliable_input').sum():,}")