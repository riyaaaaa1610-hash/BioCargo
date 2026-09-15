import requests
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


BACKEND_URL = "http://127.0.0.1:5000"

CARGO_PARAMETERS = {
    "Solid Organs": {"safe_temp": 5, "max_temp_threshold": 8},
    "Platelets": {"safe_temp": 22, "max_temp_threshold": 24},
    "Red Blood Cells": {"safe_temp": 5, "max_temp_threshold": 10},
    "Plasma & Cryo": {"safe_temp": -18, "max_temp_threshold": -18},
    "Skin, Bones, Valves": {"safe_temp": -40, "max_temp_threshold": -40},
}


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="BioCargo Viability Tracker",
    page_icon="🧬",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(135deg, #020B22, #081E3F, #031126);
        color: white;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 25px;
        padding-bottom: 45px;
    }

    h1, h2, h3, h4, p, label {
        color: white !important;
    }

    .hero {
        background: linear-gradient(135deg, #102749, #173E6A);
        border-radius: 24px;
        padding: 30px 34px;
        border: 1px solid rgba(255,255,255,.08);
        box-shadow: 0 10px 40px rgba(0,0,0,.35);
        margin-bottom: 28px;
    }

    .hero-title {
        font-size: 38px;
        font-weight: 750;
        margin: 0;
    }

    .hero-subtitle {
        color: #D7E7F7 !important;
        font-size: 16px;
        margin-top: 8px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 14px;
    }

    .card {
        background: rgba(15,35,65,.95);
        border-radius: 20px;
        padding: 22px;
        border: 1px solid rgba(255,255,255,.08);
        box-shadow: 0 8px 24px rgba(0,0,0,.25);
    }

    .metric-card {
        background: rgba(15,35,65,.95);
        border-radius: 18px;
        padding: 20px;
        min-height: 105px;
        border: 1px solid rgba(255,255,255,.08);
    }

    .metric-title {
        color: #9EC3E7 !important;
        font-size: 13px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: .06em;
    }

    .metric-value {
        color: white !important;
        font-size: 31px;
        font-weight: 750;
        margin-top: 8px;
    }

    .safe-badge, .warning-badge, .critical-badge {
        display: inline-block;
        padding: 7px 16px;
        border-radius: 30px;
        font-weight: 750;
        font-size: 14px;
    }

    .safe-badge {
        background: #00DC8C;
        color: #001b12;
    }

    .warning-badge {
        background: #F4C542;
        color: #171100;
    }

    .critical-badge {
        background: #FF4D4D;
        color: white;
    }

    .info-line {
        color: #C9D9EA !important;
        margin: 7px 0;
    }

    .big-time {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin: 10px 0;
    }

    .small-center {
        text-align: center;
        color: #AFC5DC !important;
    }

    .alert-box {
        border-radius: 18px;
        padding: 18px 22px;
        margin: 16px 0;
        border: 1px solid rgba(255,255,255,.08);
    }

    .alert-safe {
        background: rgba(0,220,140,.12);
        border-color: rgba(0,220,140,.35);
    }

    .alert-warning {
        background: rgba(244,197,66,.12);
        border-color: rgba(244,197,66,.35);
    }

    .alert-critical {
        background: rgba(255,77,77,.12);
        border-color: rgba(255,77,77,.35);
    }

    div.stButton > button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HELPERS
# =========================================================
def api_request(method, endpoint, payload=None):

    try:
        response = requests.request(
            method,
            f"{BACKEND_URL}{endpoint}",
            json=payload,
            timeout=5
        )

        try:
            body = response.json()
        except ValueError:
            body = {"error": response.text}

        return response.status_code, body

    except requests.exceptions.RequestException:
        return None, {
            "error": (
                "Backend is not running. Start app.py first "
                "using: python app.py"
            )
        }


def format_hours(hours):

    if hours is None:
        return "--"

    if hours <= 0:
        return "00:00:00"

    total_seconds = int(hours * 3600)

    days, remainder = divmod(total_seconds, 86400)
    hours_part, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days:
        return f"{days}d {hours_part:02d}:{minutes:02d}:{seconds:02d}"

    return f"{hours_part:02d}:{minutes:02d}:{seconds:02d}"


def risk_badge(risk):

    if risk == "Safe":
        return '<span class="safe-badge">SAFE</span>'

    if risk == "Warning":
        return '<span class="warning-badge">WARNING</span>'

    return '<span class="critical-badge">CRITICAL</span>'


def alert_class(risk):

    if risk == "Safe":
        return "alert-safe"

    if risk == "Warning":
        return "alert-warning"

    return "alert-critical"


def render_prediction(result):

    if not result:
        return

    viability = result["arrhenius_viability"]
    ml_viability = result["ml_viability"]
    risk = result["risk_level"]
    temperature_status = result["temperature_status"]
    safe_time = result["time_remaining_hours"]
    total_exposure = result["total_exposure_hours"]

    st.markdown('<div class="section-title">Live Cargo Status</div>',
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Arrhenius Viability</div>
                <div class="metric-value">{viability:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">ML Viability</div>
                <div class="metric-value">{ml_viability:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Exposure</div>
                <div class="metric-value">{total_exposure:.2f} hr</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Risk Level</div>
                <div style="margin-top:12px">{risk_badge(risk)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    alert_text = {
        "Safe": "Cargo is currently within the defined operating conditions.",
        "Warning": "Cargo requires close monitoring. Estimated viability is approaching the critical threshold.",
        "Critical": "Cargo has crossed the critical viability threshold. Immediate attention is required."
    }[risk]

    st.markdown(
        f"""
        <div class="alert-box {alert_class(risk)}">
            <strong>{'✓' if risk == 'Safe' else '⚠'} {risk.upper()} CARGO STATUS</strong>
            <div style="margin-top:6px;color:#D7E7F7">
                {alert_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns([1.55, 1])

    with left:

        st.markdown(
            '<div class="section-title">Biological Viability</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.progress(
            max(0.0, min(1.0, viability / 100))
        )

        st.markdown(
            f"""
            <div style="text-align:center;margin-top:15px">
                <div style="font-size:58px;font-weight:800">
                    {viability:.2f}%
                </div>
                <div style="color:#AFC5DC">
                    Arrhenius-based estimated viability
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown(
            '<div class="section-title">Estimated Safe Time</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="card">
                <div class="big-time">{format_hours(safe_time)}</div>
                <div class="small-center">
                    Remaining until estimated viability reaches 70%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="card" style="margin-top:14px">
                <div class="metric-title">Temperature Status</div>
                <div style="font-size:22px;font-weight:750;margin-top:8px">
                    {temperature_status}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Model comparison
    st.markdown(
        '<div class="section-title">Model Comparison</div>',
        unsafe_allow_html=True
    )

    model1, model2, model3 = st.columns(3)

    with model1:
        st.metric("Arrhenius Estimate", f"{viability:.2f}%")

    with model2:
        st.metric("ML Estimate", f"{ml_viability:.2f}%")

    with model3:
        st.metric(
            "Difference",
            f"{abs(viability - ml_viability):.2f} percentage points"
        )

    # Projection chart
    st.markdown(
        '<div class="section-title">Viability Projection</div>',
        unsafe_allow_html=True
    )

    # This chart is generated from the same Arrhenius result.
    # It does not pretend to be a real sensor history.
    degradation_rate = result["degradation_rate"]

    if degradation_rate > 0:
        projection_end = max(total_exposure + 1, safe_time + total_exposure + 1)
        times = np.linspace(0, projection_end, 80)
        projected = 100 * np.exp(-degradation_rate * times)
        projected = np.clip(projected, 0, 100)

        fig, ax = plt.subplots(figsize=(9, 3.5))
        ax.plot(times, projected, linewidth=2.5)
        ax.axhline(70, linestyle="--", linewidth=1.5)
        ax.axvline(total_exposure, linestyle=":", linewidth=1.5)

        ax.set_xlabel("Total Exposure Time (hours)")
        ax.set_ylabel("Estimated Viability (%)")
        ax.set_ylim(0, 105)
        ax.grid(alpha=0.18)

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # Cargo details
    st.markdown(
        '<div class="section-title">Cargo Details</div>',
        unsafe_allow_html=True
    )

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.markdown(
            f"""
            <div class="card">
                <div class="info-line"><strong>Cargo Type:</strong> {st.session_state.get('cargo_type', '--')}</div>
                <div class="info-line"><strong>Current Temperature:</strong> {st.session_state.get('current_temp', '--')}°C</div>
                <div class="info-line"><strong>Safe Temperature:</strong> {st.session_state.get('safe_temp', '--')}°C</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with detail_col2:
        st.markdown(
            f"""
            <div class="card">
                <div class="info-line"><strong>Flight Duration:</strong> {st.session_state.get('flight_duration_hours', '--')} hr</div>
                <div class="info-line"><strong>Flight Delay:</strong> {st.session_state.get('flight_delay_minutes', '--')} min</div>
                <div class="info-line"><strong>Degradation Rate:</strong> {result['degradation_rate']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# HERO
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🧬 Synthetic Biology Cargo Viability Tracker</div>
        <div class="hero-subtitle">
            AI-assisted monitoring of temperature-sensitive biological
            shipments during flight delays.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INPUT
# =========================================================
st.markdown(
    '<div class="section-title">Shipment Configuration</div>',
    unsafe_allow_html=True
)

input_left, input_right = st.columns(2)

with input_left:

    cargo_id = st.text_input(
        "Cargo ID",
        value="ORG-101"
    )

    cargo_type = st.selectbox(
        "Cargo Type",
        list(CARGO_PARAMETERS.keys())
    )

    current_temp = st.number_input(
        "Current Temperature (°C)",
        value=5.0,
        min_value=-100.0,
        max_value=100.0,
        step=0.5
    )

with input_right:

    flight_delay_minutes = st.number_input(
        "Flight Delay (minutes)",
        value=80,
        min_value=0,
        step=10
    )

    flight_duration_hours = st.number_input(
        "Flight Duration (hours)",
        value=8.0,
        min_value=0.1,
        max_value=100.0,
        step=0.5
    )

    params = CARGO_PARAMETERS[cargo_type]

    st.markdown(
        f"""
        <div class="card" style="margin-top:4px">
            <div class="metric-title">Cargo Temperature Limits</div>
            <div style="margin-top:8px">
                Safe: <strong>{params['safe_temp']}°C</strong>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                Maximum: <strong>{params['max_temp_threshold']}°C</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Keep current values available for the result section.
st.session_state["cargo_type"] = cargo_type
st.session_state["current_temp"] = current_temp
st.session_state["flight_duration_hours"] = flight_duration_hours
st.session_state["flight_delay_minutes"] = flight_delay_minutes
st.session_state["safe_temp"] = params["safe_temp"]


button1, button2, button3 = st.columns([1, 1, 1])

with button1:
    analyze = st.button(
        "⚡ Analyze Viability",
        use_container_width=True
    )

with button2:
    save = st.button(
        "💾 Save / Update Cargo",
        use_container_width=True
    )

with button3:
    refresh = st.button(
        "↻ Refresh Shipments",
        use_container_width=True
    )


# =========================================================
# ANALYZE
# =========================================================
if analyze:

    payload = {
        "cargo_type": cargo_type,
        "current_temp": current_temp,
        "flight_duration_hours": flight_duration_hours,
        "flight_delay_minutes": int(flight_delay_minutes)
    }

    status, response = api_request(
        "POST",
        "/predict",
        payload
    )

    if status == 200 and response.get("success"):
        st.session_state["prediction"] = response["data"]
        st.success("Viability analysis completed.")

    else:
        st.error(
            response.get(
                "error",
                "Unable to complete prediction."
            )
        )


# =========================================================
# SAVE / UPDATE
# =========================================================
if save:

    if not cargo_id.strip():
        st.error("Cargo ID cannot be empty.")

    else:

        payload = {
            "cargo_id": cargo_id.strip(),
            "cargo_type": cargo_type,
            "current_temp": current_temp,
            "flight_duration_hours": flight_duration_hours,
            "flight_delay_minutes": int(flight_delay_minutes)
        }

        # Check whether this cargo already exists.
        get_status, get_response = api_request(
            "GET",
            f"/cargo/{cargo_id.strip()}"
        )

        if get_status == 200 and get_response.get("success"):

            update_payload = {
                "current_temp": current_temp,
                "flight_delay_minutes": int(flight_delay_minutes),
                "flight_duration_hours": flight_duration_hours
            }

            status, response = api_request(
                "PUT",
                f"/cargo/{cargo_id.strip()}",
                update_payload
            )

        else:

            status, response = api_request(
                "POST",
                "/cargo",
                payload
            )

        if status in (200, 201) and response.get("success"):

            data = response["data"]

            # Backend prediction is authoritative.
            st.session_state["prediction"] = data

            st.success("Cargo saved and prediction updated.")

        else:

            st.error(
                response.get(
                    "error",
                    "Unable to save cargo."
                )
            )


# =========================================================
# SHOW PREDICTION
# =========================================================
render_prediction(
    st.session_state.get("prediction")
)


# =========================================================
# SHIPMENT HISTORY
# =========================================================
st.markdown(
    '<div class="section-title">Active Biological Shipments</div>',
    unsafe_allow_html=True
)

status, response = api_request("GET", "/cargo")

if status == 200 and response.get("success"):

    cargo_rows = response.get("data", [])

    if cargo_rows:

        table = pd.DataFrame(cargo_rows)

        display_columns = [
            "cargo_id",
            "cargo_type",
            "current_temp",
            "flight_duration_hours",
            "flight_delay_minutes",
            "viability_percentage",
            "risk_level"
        ]

        available_columns = [
            col for col in display_columns
            if col in table.columns
        ]

        st.dataframe(
            table[available_columns],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No cargo records found in the database.")

elif status is None:

    st.warning(
        "Backend is not connected. Start the Flask server "
        "before using database features."
    )

else:

    st.error(
        response.get(
            "error",
            "Unable to retrieve cargo records."
        )
    )
