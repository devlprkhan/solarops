import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from solarops.dashboard import load_test_predictions

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
st.title("📊 Overview")

@st.cache_data
def _load():
    return load_test_predictions()

df = _load()

start, end = st.sidebar.date_input(
    "Date range",
    value=(df["measured_on"].min().date(), df["measured_on"].max().date()),
    min_value=df["measured_on"].min().date(),
    max_value=df["measured_on"].max().date(),
)
view = df[(df["measured_on"].dt.date >= start) & (df["measured_on"].dt.date <= end)]

c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{len(view):,}")
c2.metric("Mean residual", f"{view['residual'].mean():+.1f} kW")
c3.metric("Anomaly rate", f"{(view['trust']=='anomaly').mean()*100:.2f}%")

day = view[view["poa"] > 50]
fig = go.Figure()
fig.add_trace(go.Scatter(x=day["measured_on"], y=day["actual"], name="Actual",
                         line=dict(color="#1f77b4")))
fig.add_trace(go.Scatter(x=day["measured_on"], y=day["predicted"], name="Predicted",
                         line=dict(color="#ff7f0e", dash="dash")))
fig.update_layout(title="Actual vs Predicted (daylight)", height=420, hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

day = day.assign(hour=day["measured_on"].dt.hour, month=day["measured_on"].dt.month)
pivot = day.pivot_table(index="hour", columns="month", values="residual", aggfunc="mean")
st.plotly_chart(
    px.imshow(pivot, color_continuous_scale="RdBu_r", aspect="auto",
              title="Mean residual — hour × month"),
    use_container_width=True,
)