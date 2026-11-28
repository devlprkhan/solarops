import streamlit as st
from solarops.dashboard import load_test_predictions, get_anomalies

st.set_page_config(page_title="Anomalies", page_icon="🚨", layout="wide")
st.title("🚨 Anomalies")

@st.cache_data
def _load():
    return load_test_predictions()

df = _load()

n = st.slider("How many?", 10, 100, 20, step=10)
a = get_anomalies(df, n=n)

st.metric("Showing", f"{len(a)} anomalies")
st.dataframe(a, use_container_width=True, height=500)

st.download_button(
    "📥 Download as CSV",
    a.to_csv(index=False),
    file_name="solarops_anomalies.csv",
    mime="text/csv",
)