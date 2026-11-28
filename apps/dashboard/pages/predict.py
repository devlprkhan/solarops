"""Predict — try the model yourself with custom inputs."""

import os
from datetime import date

import httpx
import plotly.express as px
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT = 10.0

st.set_page_config(page_title="Predict", page_icon="🔮", layout="wide")
st.title("🔮 Predict — try the model")
st.caption("Enter solar conditions, get expected AC power.")

# Backend availability check
try:
    with httpx.Client(timeout=TIMEOUT) as client:
        r = client.get(f"{API_BASE_URL}/health")
        r.raise_for_status()
except Exception as exc:  # noqa: BLE001
    st.warning(f"Backend unavailable ({exc}). Start the API to enable predictions.")

with st.form("predict_form"):
    c1, c2 = st.columns(2)
    with c1:
        poa = st.slider("POA irradiance (W/m²)", 0, 1100, 700)
        temp = st.slider("Ambient temperature (°C)", -10.0, 50.0, 25.0)
    with c2:
        wind = st.slider("Wind speed (m/s)", 0.0, 20.0, 3.0)
        d = st.date_input("Date", date(2024, 6, 15))
    hour = st.slider("Hour of day", 0, 23, 12)
    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "poa_irradiance": poa,
        "ambient_temperature": temp,
        "wind_speed": wind,
        "hour": hour,
        "month": d.month,
        "dayofyear": d.timetuple().tm_yday,
    }
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            r = client.post(f"{API_BASE_URL}/predict", json=payload)
            r.raise_for_status()
            result = r.json()
    except httpx.HTTPStatusError as exc:
        st.error(f"Prediction request failed: {exc.response.text}")
        result = None
    except Exception as exc:  # noqa: BLE001
        st.error(f"Could not reach backend: {exc}")
        result = None

    if result is not None:
        st.metric("Predicted AC power", f"{result['predicted_ac_power']:.1f} kW")
        st.caption(
            f"Model {result.get('model_version')} · via FastAPI backend"
        )

        st.subheader("Prediction curve at this POA (across the day)")
        preds = []
        for h in range(24):
            p = dict(payload, hour=h)
            try:
                with httpx.Client(timeout=TIMEOUT) as client:
                    rr = client.post(f"{API_BASE_URL}/predict", json=p)
                    rr.raise_for_status()
                    preds.append(rr.json()["predicted_ac_power"])
            except Exception:  # noqa: BLE001
                preds.append(None)
        fig = px.line(x=list(range(24)), y=preds, labels={"x": "Hour of day", "y": "Predicted kW"})
        fig.add_scatter(x=[hour], y=[result["predicted_ac_power"]], mode="markers",
                        marker=dict(size=18, color="red", symbol="star"), name="You")
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Why is hour important?"):
        st.markdown(
            "Same POA at 9 AM vs 2 PM produces different power — "
            "the sun's angle and panel temperature lag differ. "
            "That's why `hour` is a feature."
        )