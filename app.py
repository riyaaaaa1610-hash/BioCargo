import streamlit as st
from prediction import get_prediction

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="BioCargo Tracker",
    page_icon="🧬",
    layout="wide"
)

# ---------------- LOAD CSS ---------------- #
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- HERO HEADER ---------------- #
st.markdown("""
<div class="hero">
    <h1>🧬 Synthetic Biology Cargo Viability Tracker</h1>
    <p>Real-time monitoring for temperature-sensitive biological cargo during flight delays.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT SECTION ---------------- #
st.markdown('<div class="section-title">Cargo Input</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
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

with col2:
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

# ---------------- BACKEND PREDICTION ---------------- #
try:
    result = get_prediction(
        cargo_type=cargo_type,
        current_temp=current_temp,
        flight_delay_minutes=flight_delay_minutes
    )

    viability_percentage = result["viability_percentage"]
    risk_level = result["risk_level"]

except ValueError as e:
    st.error(str(e))
    st.stop()

# ---------------- STATUS CARDS ---------------- #
st.markdown("---")
st.markdown('<div class="section-title">Live Cargo Status</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">BIOLOGICAL VIABILITY</div>
        <div class="metric-value">{viability_percentage}%</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">FLIGHT DELAY</div>
        <div class="metric-value">{flight_delay_minutes} min</div>
    </div>
    """, unsafe_allow_html=True)

with c3:

    status_class = "safe"

    if risk_level.lower() == "warning":
        status_class = "warning"
    elif risk_level.lower() != "safe":
        status_class = "critical"

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">RISK LEVEL</div>
        <div class="metric-value {status_class}">{risk_level}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- VIABILITY BAR ---------------- #
st.markdown("---")
st.markdown('<div class="section-title">Viability Monitor</div>', unsafe_allow_html=True)

st.progress(viability_percentage / 100)

# ---------------- DETAILS ---------------- #
st.markdown("---")

left, right = st.columns([2, 1])

with left:

    st.markdown('<div class="section-title">Cargo Details</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="input-box">

    **Cargo ID:** {cargo_id}

    **Cargo Type:** {cargo_type}

    **Current Temperature:** {current_temp}°C

    **Flight Delay:** {flight_delay_minutes} minutes

    </div>
    """, unsafe_allow_html=True)

with right:

    st.markdown('<div class="section-title">Operational Status</div>', unsafe_allow_html=True)

    if risk_level.lower() == "safe":
        st.markdown('<div class="badge-safe">SAFE</div>', unsafe_allow_html=True)
        st.success("Cargo remains within safe operating conditions.")

    elif risk_level.lower() == "warning":
        st.markdown('<div class="badge-warning">WARNING</div>', unsafe_allow_html=True)
        st.warning("Monitor the shipment closely.")

    else:
        st.markdown('<div class="badge-critical">CRITICAL</div>', unsafe_allow_html=True)
        st.error("Immediate intervention required.")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("BioCargo • AI-assisted Cold Chain Monitoring • VMEDITHON 3.0")