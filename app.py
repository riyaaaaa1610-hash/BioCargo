import streamlit as st
from prediction import get_prediction
from streamlit_echarts import st_echarts
import matplotlib.pyplot as plt
import numpy as np

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="BioCargo Tracker",
    page_icon="🧬",
    layout="wide"
)

# ---------------- LOAD CSS ---------------- #
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- HERO ---------------- #
st.markdown("""
<div class="hero">
    <h1>🧬 Synthetic Biology Cargo Viability Tracker</h1>
    <p>Real-time monitoring of temperature-sensitive biological shipments during flight delays.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT SECTION ---------------- #
st.markdown("## Cargo Input")

left, right = st.columns(2)

with left:
    cargo_id = st.text_input("Cargo ID", "ORG-101")

    cargo_type = st.selectbox(
        "Cargo Type",
        [
            "Solid Organs",
            "Platelets",
            "Red Blood Cells",
            "Plasma & Cryo",
            "Skin, Bones, Valves"
        ]
    )

with right:
    current_temp = st.number_input(
        "Current Temperature (°C)",
        value=5.0,
        step=1.0
    )

    flight_delay_minutes = st.number_input(
        "Flight Delay (Minutes)",
        min_value=0,
        value=120,
        step=10
    )

    flight_duration_hours = st.number_input(
        "Flight Duration (Hours)",
        min_value=0.5,
        value=2.0,
        step=0.5
    )

# ---------------- BACKEND PREDICTION ---------------- #
try:
    result = get_prediction(
        cargo_type=cargo_type,
        current_temp=current_temp,
        flight_delay_minutes=flight_delay_minutes,
        flight_duration_hours=flight_duration_hours
    )

    # Compatible with different backend key names
    viability = (
        result.get("viability_percentage")
        or result.get("viability")
        or result.get("biological_viability")
        or 0
    )

    risk = (
        result.get("risk_level")
        or result.get("risk")
        or "Unknown"
    )

except Exception as e:
    st.error(f"Backend Error: {e}")
    st.stop()

# ---------------- STATUS CARDS ---------------- #
st.markdown("---")
st.markdown("## Live Cargo Status")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">VIABILITY</div>
        <div class="metric-value">{viability}%</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">DELAY</div>
        <div class="metric-value">{flight_delay_minutes} min</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">DURATION</div>
        <div class="metric-value">{flight_duration_hours} hr</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    badge = "safe"

    if str(risk).lower() == "warning":
        badge = "warning"
    elif str(risk).lower() in ["critical", "high", "high/critical"]:
        badge = "critical"

    st.markdown(f"""
    <div class="card">
        <div class="metric-title">RISK LEVEL</div>
        <div class="{badge}">{risk}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- GAUGE & COUNTDOWN ---------------- #
st.markdown("---")

left, right = st.columns([2, 1])

with left:
    st.markdown("### Biological Viability")

    option = {
        "series": [{
            "type": "gauge",
            "progress": {"show": True},
            "axisLine": {"lineStyle": {"width": 18}},
            "detail": {"formatter": "{value}%", "fontSize": 28},
            "data": [{"value": viability}]
        }]
    }

    st_echarts(option, height="320px")

with right:
    st.markdown("### Estimated Safe Time")

    hours = max(0, (100 - int(viability)) // 10 + 1)

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h1>{hours}:00:00</h1>
        <p>Remaining Safe Window</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- TEMPERATURE TREND ---------------- #
st.markdown("---")

left, right = st.columns(2)

with left:
    st.markdown("### Temperature Trend")

    temps = np.linspace(current_temp, current_temp + 4, 6)

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(range(6), temps, marker="o", linewidth=3)
    ax.set_facecolor("#0F2341")
    fig.patch.set_facecolor("#0F2341")
    ax.tick_params(colors="white")
    ax.spines[:].set_color("white")
    ax.set_ylabel("Temperature (°C)", color="white")
    ax.set_xlabel("Time", color="white")

    st.pyplot(fig)

with right:
    st.markdown("### Cargo Details")

    st.markdown(f"""
    <div class="card">

    **Cargo ID:** {cargo_id}

    **Cargo Type:** {cargo_type}

    **Current Temperature:** {current_temp}°C

    **Flight Delay:** {flight_delay_minutes} minutes

    **Flight Duration:** {flight_duration_hours} hours

    </div>
    """, unsafe_allow_html=True)

# ---------------- OPERATIONAL STATUS ---------------- #
st.markdown("---")
st.markdown("### Operational Status")

if str(risk).lower() == "safe":
    st.success("🟢 Cargo is within safe operating conditions.")
elif str(risk).lower() == "warning":
    st.warning("🟡 Cargo requires close monitoring.")
else:
    st.error("🔴 Immediate intervention required.")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("BioCargo • AI-powered Cold Chain Monitoring • VMEDITHON 3.0")