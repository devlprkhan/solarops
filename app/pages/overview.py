import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from solarops.dashboard import load_test_predictions, get_anomalies
from solarops.ui import (
    inject_styles,
    page_header,
    style_figure,
    COLOR_ACTUAL,
    COLOR_PREDICTED,
    COLOR_ANOMALY,
)

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
inject_styles()
page_header("Overview", "Solar system performance at a glance.")

@st.cache_data
def _load():
    return load_test_predictions()

df = _load()

# ---- Filters (sidebar) ----
start, end = st.sidebar.date_input(
    "Date range",
    value=(df["measured_on"].min().date(), df["measured_on"].max().date()),
    min_value=df["measured_on"].min().date(),
    max_value=df["measured_on"].max().date(),
)
view = df[(df["measured_on"].dt.date >= start) & (df["measured_on"].dt.date <= end)]

# ---- Key metrics ----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{len(view):,}")
c2.metric("Mean residual", f"{view['residual'].mean():+.1f} kW")
c3.metric("Anomaly rate", f"{(view['trust']=='anomaly').mean()*100:.2f}%")
c4.metric("Unreliable inputs", f"{(view['trust']=='unreliable_input').sum():,}")

# ---- Trust status chips ----
ok_n = int((view["trust"] == "ok").sum())
anom_n = int((view["trust"] == "anomaly").sum())
unrel_n = int((view["trust"] == "unreliable_input").sum())
chip_cols = st.columns(3)
with chip_cols[0]:
    st.badge(f"Normal · {ok_n:,}", color="green")
with chip_cols[1]:
    st.badge(f"Anomaly · {anom_n:,}", color="red")
with chip_cols[2]:
    st.badge(f"Unreliable input · {unrel_n:,}", color="gray")

# ---- Expected vs actual (prominent) ----
day = view[view["poa"] > 50]
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=day["measured_on"], y=day["actual"], name="Actual",
    line=dict(color=COLOR_ACTUAL, width=1.6),
))
fig.add_trace(go.Scatter(
    x=day["measured_on"], y=day["predicted"], name="Predicted (expected)",
    line=dict(color=COLOR_PREDICTED, width=1.6, dash="dash"),
))
style_figure(fig, title="Actual vs predicted AC power (daylight)", height=440)
fig.update_layout(hovermode="x unified", yaxis_title="AC power (kW)")
st.plotly_chart(fig, use_container_width=True)

# ---- Trust status area + supporting trend ----
left, right = st.columns([1, 1])
with left:
    st.subheader("Performance status")
    st.metric("Normal rows", f"{ok_n:,}")
    st.metric("Anomaly rows", f"{anom_n:,}")
    st.metric("Unreliable rows", f"{unrel_n:,}")

with right:
    day2 = day.assign(hour=day["measured_on"].dt.hour, month=day["measured_on"].dt.month)
    pivot = day2.pivot_table(index="hour", columns="month", values="residual", aggfunc="mean")
    heat = px.imshow(
        pivot, color_continuous_scale="RdBu_r", aspect="auto",
        title="Mean residual — hour × month",
    )
    style_figure(heat, title="Mean residual — hour × month", height=360)
    st.plotly_chart(heat, use_container_width=True)

# ---- Recent items needing attention ----
st.subheader("Recent items that may need attention")
anoms = get_anomalies(df, n=5)
if anoms.empty:
    st.markdown('<div class="so-empty">No anomalies found in the current dataset.</div>', unsafe_allow_html=True)
else:
    show = anoms[["measured_on", "actual", "predicted", "residual", "trust"]].copy()
    st.dataframe(
        show,
        use_container_width=True,
        hide_index=True,
        column_config={
            "measured_on": st.column_config.DatetimeColumn("Time", format="YYYY-MM-DD HH:mm"),
            "actual": st.column_config.NumberColumn("Actual (kW)", format="%.1f"),
            "predicted": st.column_config.NumberColumn("Expected (kW)", format="%.1f"),
            "residual": st.column_config.NumberColumn("Residual (kW)", format="%+.1f"),
            "trust": st.column_config.TextColumn("Status"),
        },
    )