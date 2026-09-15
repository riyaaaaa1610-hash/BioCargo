import streamlit as st
from prediction import get_prediction

# ---------------- PAGE ---------------- #
st.set_page_config(
    page_title="BioCargo Tracker",
    page_icon="🧬",
    layout="wide"
)

# ---------------- TITLE ---------------- #
st.title("🧬 Synthetic Biology Cargo Viability Tracker")
st.caption("Real-time monitoring for temperature-sensitive biological cargo.")

# ---------------- INPUT VARIABLES ---------------- #
cargo_id = st.text_input("Cargo ID", "ORG-101")

cargo_type = st.selectbox(
    "Cargo Type",
    ["Live Organ", "mRNA Vaccine", "Cell Culture", "Blood Sample"]
)

current_temp = st.number_input(
    "Current Temperature (°C)",
    value=-2.0
)

flight_delay_minutes = st.number_input(
    "Flight Delay (Minutes)",
    min_value=0,
    value=120
)

# ---------------- CALL BACKEND ---------------- #
result = get_prediction(
    cargo_type=cargo_type,
    current_temp=current_temp,
    flight_delay_minutes=flight_delay_minutes
)

# Values returned by prediction.py
viability_percentage = result["viability_percentage"]
risk_level = result["risk_level"]

# ---------------- DASHBOARD ---------------- #
st.markdown("---")
st.subheader("Cargo Status")

st.metric("Viability", f"{viability_percentage}%")
st.metric("Flight Delay", f"{flight_delay_minutes} min")
st.metric("Risk Level", risk_level)

# ---------------- DETAILS ---------------- #
st.markdown("---")
st.subheader("Cargo Details")

st.write(f"**Cargo ID:** {cargo_id}")
st.write(f"**Cargo Type:** {cargo_type}")
st.write(f"**Current Temperature:** {current_temp}°C")

# ---------------- ALERT ---------------- #
if risk_level == "Safe":
    st.success("Cargo is within safe operating conditions.")
elif risk_level == "Warning":
    st.warning("Cargo requires close monitoring.")
else:
    st.error("Critical: Immediate intervention required.")