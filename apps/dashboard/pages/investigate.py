import streamlit as st
import plotly.graph_objects as go
from solarops.dashboard import load_test_predictions

st.set_page_config(page_title="Investigate", page_icon="🔍", layout="wide")
st.title("🔍 Investigate a day")

@st.cache_data
def _load():
    return load_test_predictions()

df = _load()

target = st.date_input("Pick a date", df["measured_on"].dt.date.max())
d = df[df["measured_on"].dt.date == target]

if d.empty:
    st.warning("No rows on that date.")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Production", f"{d['actual'].sum()/4:,.1f} kWh")
    c2.metric("Mean residual", f"{d['residual'].mean():+.1f} kW")
    c3.metric("Anomalies", f"{(d['trust']=='anomaly').sum()}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d["measured_on"], y=d["actual"], name="Actual"))
    fig.add_trace(go.Scatter(x=d["measured_on"], y=d["predicted"], name="Predicted",
                             line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=d["measured_on"], y=d["poa"], name="POA",
                             yaxis="y2", opacity=0.35))
    fig.update_layout(
        height=420, hovermode="x unified",
        yaxis=dict(title="AC power (kW)"),
        yaxis2=dict(title="POA (W/m²)", overlaying="y", side="right", showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(d, use_container_width=True)