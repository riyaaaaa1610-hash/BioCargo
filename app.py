import streamlit as st
from prediction import get_prediction
from streamlit_echarts import st_echarts
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="BioCargo",
    page_icon="🧬",
    layout="wide"
)

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
<h1>🧬 Synthetic Biology Cargo Viability Tracker</h1>
<p>Real-time monitoring of temperature-sensitive biological shipments during flight delays.</p>
</div>
""", unsafe_allow_html=True)

# Input

left,right=st.columns(2)

with left:

    cargo_id=st.text_input("Cargo ID","ORG-101")

    cargo_type=st.selectbox(
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

    current_temp=st.number_input(
        "Current Temperature (°C)",
        value=5.0
    )

    flight_delay_minutes=st.number_input(
        "Flight Delay (Minutes)",
        value=120
    )

# Prediction

result=get_prediction(
    cargo_type=cargo_type,
    current_temp=current_temp,
    flight_delay_minutes=flight_delay_minutes
)

viability=result["viability_percentage"]
risk=result["risk_level"]

# KPI Cards

st.markdown("## Live Status")

c1,c2,c3=st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">VIABILITY</div>
        <div class="metric-value">{viability}%</div>
    </div>
    """,unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-title">FLIGHT DELAY</div>
        <div class="metric-value">{flight_delay_minutes} min</div>
    </div>
    """,unsafe_allow_html=True)

with c3:

    color="safe"

    if risk=="Warning":
        color="warning"

    elif risk=="Critical":
        color="critical"

    st.markdown(f"""
    <div class="card">
        <div class="metric-title">RISK LEVEL</div>
        <div class="{color}">{risk}</div>
    </div>
    """,unsafe_allow_html=True)

st.markdown("---")

# Gauge + Timer

left,right=st.columns([2,1])

with left:

    st.markdown("### Biological Viability")

    option={
        "series":[{
            "type":"gauge",
            "progress":{"show":True},
            "axisLine":{"lineStyle":{"width":18}},
            "detail":{"formatter":"{value}%","fontSize":28},
            "data":[{"value":viability}]
        }]
    }

    st_echarts(option,height="320px")

with right:

    st.markdown("### Countdown")

    hours=max(0,(100-viability)//10+1)

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h1>{hours}:00:00</h1>
        <p>Estimated Safe Time</p>
    </div>
    """,unsafe_allow_html=True)

# Charts

st.markdown("---")

left,right=st.columns(2)

with left:

    st.markdown("### Temperature Trend")

    temps=np.linspace(current_temp,current_temp+4,6)

    fig,ax=plt.subplots(figsize=(5,3))
    ax.plot(temps,marker="o",linewidth=3)
    ax.set_facecolor("#0F2341")
    fig.patch.set_facecolor("#0F2341")
    ax.tick_params(colors="white")
    ax.spines[:].set_color("white")
    ax.set_ylabel("°C",color="white")

    st.pyplot(fig)

with right:

    st.markdown("### Cargo Details")

    st.markdown(f"""
    <div class="card">

    **Cargo ID**

    {cargo_id}

    **Cargo Type**

    {cargo_type}

    **Current Temperature**

    {current_temp}°C

    **Flight Delay**

    {flight_delay_minutes} minutes

    </div>
    """,unsafe_allow_html=True)

# Footer

st.markdown("---")
st.caption("BioCargo • AI-powered Cold Chain Monitoring • VMEDITHON 3.0")