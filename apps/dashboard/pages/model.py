import streamlit as st
import plotly.express as px
from solarops.dashboard import load_test_predictions, get_model_card

st.set_page_config(page_title="Model", page_icon="⚙️", layout="wide")
st.title("⚙️ Model")

@st.cache_data
def _load():
    return load_test_predictions()

df = _load()
card = get_model_card()

st.subheader("Model card")
st.json(card)

st.subheader("Residual distribution")
st.plotly_chart(
    px.histogram(df, x="residual", nbins=80, title="Residual (kW)"),
    use_container_width=True,
)