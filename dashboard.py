import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ---------------- STATUS CARDS ---------------- #
def show_status_cards():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Shipments", "24")

    with col2:
        st.metric("Safe", "18")

    with col3:
        st.metric("Warning", "4")

    with col4:
        st.metric("Critical", "2")


# ---------------- CARGO TABLE ---------------- #
def show_cargo_table():

    data = pd.DataFrame({
        "cargo_id": ["ORG-101", "VAC-205", "CELL-310"],
        "cargo_type": ["Live Organ", "mRNA Vaccine", "Cell Culture"],
        "current_temp": [-2, -15, 8],
        "flight_delay_minutes": [120, 80, 160],
        "viability_percentage": [96, 82, 61],
        "risk_level": ["Safe", "Warning", "Critical"]
    })

    st.subheader("Active Biological Shipments")
    st.dataframe(data, use_container_width=True)


# ---------------- SELECTED CARGO ---------------- #
def show_selected_cargo():

    st.subheader("Selected Shipment")

    cargo_id = "ORG-101"
    cargo_type = "Live Organ"
    current_temp = -2
    safe_temp = -20
    max_temp_threshold = 5
    flight_delay_minutes = 120
    viability_percentage = 96
    decay_rate = 0.05
    time_remaining_hours = 4
    risk_level = "Safe"

    st.write(f"**Cargo ID:** {cargo_id}")
    st.write(f"**Cargo Type:** {cargo_type}")
    st.write(f"**Current Temperature:** {current_temp}°C")
    st.write(f"**Safe Temperature:** {safe_temp}°C")
    st.write(f"**Maximum Threshold:** {max_temp_threshold}°C")
    st.write(f"**Flight Delay:** {flight_delay_minutes} min")
    st.write(f"**Viability:** {viability_percentage}%")
    st.write(f"**Decay Rate:** {decay_rate}")
    st.write(f"**Remaining Safe Time:** {time_remaining_hours} hrs")
    st.write(f"**Risk Level:** {risk_level}")


# ---------------- VIABILITY SECTION ---------------- #
def show_viability_section():

    st.subheader("Biological Viability")

    viability_percentage = 96
    time_remaining_hours = 4

    st.progress(viability_percentage / 100)

    st.metric("Viability", f"{viability_percentage}%")
    st.metric("Remaining Safe Time", f"{time_remaining_hours} hrs")


# ---------------- ALERTS ---------------- #
def show_alert_banner():

    risk_level = "Critical"

    if risk_level == "Safe":
        st.success("Cargo is within safe operating conditions.")

    elif risk_level == "Warning":
        st.warning("Cargo requires close monitoring.")

    else:
        st.error("Critical: Immediate intervention required.")


# ---------------- CHARTS ---------------- #
def show_charts():

    st.subheader("Temperature Trend")

    current_temp = [-20, -18, -15, -10]

    fig, ax = plt.subplots()
    ax.plot(current_temp, marker="o")
    ax.set_ylabel("Temperature (°C)")
    st.pyplot(fig)

    st.subheader("Viability Trend")

    viability_percentage = [100, 98, 94, 88]

    fig2, ax2 = plt.subplots()
    ax2.plot(viability_percentage, marker="o")
    ax2.set_ylabel("Viability (%)")
    st.pyplot(fig2)
