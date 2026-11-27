import streamlit as st

from solarops.dashboard import load_test_predictions, get_anomalies
from solarops.ui import inject_styles, page_header, style_figure

st.set_page_config(page_title="Anomalies", page_icon="🚨", layout="wide")
inject_styles()
page_header("Anomalies", "Periods where actual output differs meaningfully from expected output.")

@st.cache_data
def _load():
    return load_test_predictions()

df = _load()

# ---- Filters ----
with st.container():
    f1, f2 = st.columns([1, 2])
    with f1:
        n = st.slider("How many to show", 10, 100, 20, step=10)
    with f2:
        st.markdown(
            '<p class="so-subtitle" style="margin-top:1.6rem;">'
            "Anomalies are rows with present inputs and |residual| ≥ 200 kW. "
            "A large residual is a signal to investigate, not proof of a fault."
            '</p>',
            unsafe_allow_html=True,
        )

a = get_anomalies(df, n=n)

# ---- Summary ----
m1, m2, m3 = st.columns(3)
m1.metric("Showing", f"{len(a)}")
m2.metric("Total anomalies", f"{(df['trust']=='anomaly').sum():,}")
m3.metric("Unreliable inputs", f"{(df['trust']=='unreliable_input').sum():,}")

if a.empty:
    st.markdown('<div class="so-empty">No anomalies found. All measured periods are within tolerance.</div>', unsafe_allow_html=True)
else:
    show = a[["measured_on", "actual", "predicted", "residual", "trust", "poa"]].copy()
    st.dataframe(
        show,
        use_container_width=True,
        hide_index=True,
        height=500,
        column_config={
            "measured_on": st.column_config.DatetimeColumn("Time", format="YYYY-MM-DD HH:mm"),
            "actual": st.column_config.NumberColumn("Measured (kW)", format="%.1f"),
            "predicted": st.column_config.NumberColumn("Expected (kW)", format="%.1f"),
            "residual": st.column_config.NumberColumn("Deviation (kW)", format="%+.1f"),
            "trust": st.column_config.TextColumn("Status"),
            "poa": st.column_config.NumberColumn("POA (W/m²)", format="%.0f"),
        },
    )

    st.download_button(
        "Download as CSV",
        a.to_csv(index=False),
        file_name="solarops_anomalies.csv",
        mime="text/csv",
    )