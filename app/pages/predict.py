"""Predict — try the model yourself with custom inputs."""

import streamlit as st
import plotly.express as px
from datetime import date

from solarops.dashboard import predict_one, get_model_card
from solarops.ui import inject_styles, page_header, style_figure, COLOR_PREDICTED

st.set_page_config(page_title="Predict", page_icon="🔮", layout="wide")
inject_styles()
page_header("Predict", "Obtain an expected AC power prediction from solar conditions.")

card = get_model_card()

with st.form("predict_form"):
    st.markdown("**Environmental and system inputs**")
    c1, c2 = st.columns(2)
    with c1:
        poa = st.slider("POA irradiance (W/m²)", 0, 1100, 700, help="Plane-of-array irradiance.")
        temp = st.slider("Ambient temperature (°C)", -10.0, 50.0, 25.0)
    with c2:
        wind = st.slider("Wind speed (m/s)", 0.0, 20.0, 3.0)
        d = st.date_input("Date", date(2024, 6, 15))
    hour = st.slider("Hour of day", 0, 23, 12)
    submitted = st.form_submit_button("Predict")

if submitted:
    doy = d.timetuple().tm_yday
    pred, meta = predict_one(poa, temp, wind, hour, d.month, doy)

    st.metric("Predicted AC power", f"{pred:.1f} kW")
    st.caption(
        f"Model {meta['version']} · MAE {meta['metrics']['MAE']:.1f} kW · "
        f"R² {meta['metrics']['R2']:.3f}"
    )

    st.subheader("Prediction curve at this POA (across the day)")
    hours = list(range(24))
    preds = [predict_one(poa, temp, wind, h, d.month, doy)[0] for h in hours]
    fig = px.line(
        x=hours, y=preds,
        labels={"x": "Hour of day", "y": "Predicted (kW)"},
    )
    fig.add_scatter(
        x=[hour], y=[pred], mode="markers",
        marker=dict(size=14, color="#B33A3A", symbol="star"), name="Selected hour",
    )
    style_figure(fig, title=f"At POA={poa:.0f} W/m², temp={temp:.0f}°C, wind={wind:.1f} m/s", height=380)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Why is hour important?"):
        st.markdown(
            "Same POA at 9 AM vs 2 PM produces different power — "
            "the sun's angle and panel temperature lag differ. "
            "That is why `hour` is a feature."
        )