import streamlit as st
from prediction import get_prediction

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="BioCargo Tracker",
    page_icon="🧬",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
.stApp{
    background-color:#081224;
    color:white;
}

h1,h2,h3{
    color:white;
}

.subtitle{
    color:#B0B7C3;
    font-size:18px;
}

div[data-testid="stMetric"]{
    background:#0F2341;
    padding:15px;
    border-radius:12px;
    border:1px solid #1E3A5F;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.title("🧬 Synthetic Biology Cargo Viability Tracker")
st.markdown(
    '<p class="subtitle">Real-time monitoring for temperature-sensitive biological cargo during flight delays.</p>',
    unsafe_allow_html=True
)

# ---------------- INPUTS ---------------- #
cargo_id = st.text_input("Cargo ID", "ORG-101")

# Display names → Backend values
cargo_options = {
    "Live Organ": "live_organ",
    "mRNA Vaccine": "mrna_vaccine",
    "Cell Culture": "cell_culture",
    "Blood Sample": "blood_sample"
}

cargo_display = st.selectbox(
    "Cargo Type",
    list(cargo_options.keys())
)

cargo_type = cargo_options[cargo_display]

current_temp = st.number_input(
    "Current Temperature (°C)",
    value=-2.0
)

flight_delay_minutes = st.number_input(
    "Flight Delay (Minutes)",
    min_value=0,
    value=120
)

# ---------------- PREDICTION ---------------- #
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

# ---------------- DASHBOARD ---------------- #
st.markdown("---")
st.subheader("Cargo Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Viability", f"{viability_percentage}%")

with col2:
    st.metric("Flight Delay", f"{flight_delay_minutes} min")

with col3:
    st.metric("Risk Level", risk_level)

# ---------------- CARGO DETAILS ---------------- #
st.markdown("---")
st.subheader("Cargo Details")

st.write(f"**Cargo ID:** {cargo_id}")
st.write(f"**Cargo Type:** {cargo_display}")
st.write(f"**Current Temperature:** {current_temp}°C")

# ---------------- VIABILITY BAR ---------------- #
st.markdown("---")
st.subheader("Biological Viability")

st.progress(viability_percentage / 100)

# ---------------- ALERTS ---------------- #
st.markdown("---")

if risk_level.lower() == "safe":
    st.success("🟢 Cargo is within safe operating conditions.")

elif risk_level.lower() == "warning":
    st.warning("🟡 Cargo requires close monitoring.")

else:
    st.error("🔴 Critical: Immediate intervention required.")