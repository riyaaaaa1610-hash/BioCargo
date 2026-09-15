import streamlit as st

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

safe_temp = st.number_input(
    "Safe Temperature (°C)",
    value=-20.0
)

max_temp_threshold = st.number_input(
    "Maximum Temperature Threshold (°C)",
    value=5.0
)

flight_delay_minutes = st.number_input(
    "Flight Delay (Minutes)",
    min_value=0,
    value=120
)

viability_percentage = st.slider(
    "Biological Viability (%)",
    min_value=0,
    max_value=100,
    value=94
)

decay_rate = st.number_input(
    "Decay Rate",
    value=0.05
)

time_remaining_hours = st.number_input(
    "Remaining Safe Time (Hours)",
    value=4.0
)

risk_level = st.selectbox(
    "Risk Level",
    ["Safe", "Warning", "Critical"]
)

# ---------------- DASHBOARD ---------------- #
st.markdown("---")
st.subheader("Cargo Status")

st.metric("Viability", f"{viability_percentage}%")
st.metric("Remaining Safe Time", f"{time_remaining_hours} hrs")
st.metric("Flight Delay", f"{flight_delay_minutes} min")

st.markdown("---")
st.subheader("Cargo Details")

st.write(f"**Cargo ID:** {cargo_id}")
st.write(f"**Cargo Type:** {cargo_type}")
st.write(f"**Current Temperature:** {current_temp}°C")
st.write(f"**Safe Temperature:** {safe_temp}°C")
st.write(f"**Maximum Threshold:** {max_temp_threshold}°C")
st.write(f"**Decay Rate:** {decay_rate}")
st.write(f"**Risk Level:** {risk_level}")

# ---------------- ALERT ---------------- #
if risk_level == "Safe":
    st.success("Cargo is within safe operating conditions.")

elif risk_level == "Warning":
    st.warning("Cargo requires close monitoring.")

else:
    st.error("Critical: Immediate intervention required.")
