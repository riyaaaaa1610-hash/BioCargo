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
background:linear-gradient(135deg,#020B22,#081E3F,#031126);
color:white;
}

.main>.block-container{
padding-top:2rem;
padding-bottom:2rem;
max-width:1200px;
}

.hero{
background:linear-gradient(135deg,#0F2341,#17345F);
padding:25px;
border-radius:20px;
border:1px solid rgba(255,255,255,.08);
margin-bottom:25px;
box-shadow:0 8px 30px rgba(0,0,0,.35);
}

.hero h1{
color:white;
font-size:42px;
margin:0;
}

.hero p{
color:#C8D6E5;
font-size:18px;
margin-top:8px;
}

.metric-card{
background:#0F2341;
padding:20px;
border-radius:18px;
text-align:center;
border:1px solid rgba(255,255,255,.08);
box-shadow:0 6px 18px rgba(0,0,0,.25);
}

.metric-title{
font-size:14px;
color:#AFC3DA;
}

.metric-value{
font-size:32px;
font-weight:bold;
color:white;
}

.safe{
color:#00DC8C;
font-weight:bold;
}

.warning{
color:#F4C542;
font-weight:bold;
}

.critical{
color:#FF4D4D;
font-weight:bold;
}

.input-box{
background:#0F2341;
padding:18px;
border-radius:18px;
border:1px solid rgba(255,255,255,.08);
}

.section-title{
font-size:24px;
font-weight:bold;
margin-bottom:15px;
}

hr{
border:1px solid rgba(255,255,255,.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.markdown("""
<div class="hero">
<h1>🧬 Synthetic Biology Cargo Viability Tracker</h1>
<p>Real-time monitoring for temperature-sensitive biological cargo during flight delays.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUTS ---------------- #
st.markdown('<div class="section-title">Cargo Input</div>', unsafe_allow_html=True)

col1,col2=st.columns(2)

with col1:
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

with col2:
    current_temp=st.number_input(
        "Current Temperature (°C)",
        value=5.0
    )

    flight_delay_minutes=st.number_input(
        "Flight Delay (Minutes)",
        min_value=0,
        value=120
    )

# ---------------- PREDICTION ---------------- #
result=get_prediction(
    cargo_type=cargo_type,
    current_temp=current_temp,
    flight_delay_minutes=flight_delay_minutes
)

viability_percentage=result["viability_percentage"]
risk_level=result["risk_level"]

# ---------------- STATUS CARDS ---------------- #
st.markdown("---")

col1,col2,col3=st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Viability</div>
    <div class="metric-value">{viability_percentage}%</div>
    </div>
    """,unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Flight Delay</div>
    <div class="metric-value">{flight_delay_minutes} min</div>
    </div>
    """,unsafe_allow_html=True)

with col3:

    color="safe"

    if risk_level.lower()=="warning":
        color="warning"

    elif risk_level.lower()!="safe":
        color="critical"

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">Risk Level</div>
    <div class="metric-value {color}">{risk_level}</div>
    </div>
    """,unsafe_allow_html=True)

# ---------------- VIABILITY ---------------- #
st.markdown("---")
st.markdown('<div class="section-title">Biological Viability</div>',unsafe_allow_html=True)

st.progress(viability_percentage/100)

# ---------------- DETAILS ---------------- #
st.markdown("---")

col1,col2=st.columns([2,1])

with col1:

    st.markdown('<div class="section-title">Cargo Details</div>',unsafe_allow_html=True)

    st.markdown(f"""
    <div class="input-box">

    **Cargo ID:** {cargo_id}

    **Cargo Type:** {cargo_type}

    **Current Temperature:** {current_temp}°C

    **Flight Delay:** {flight_delay_minutes} minutes

    </div>
    """,unsafe_allow_html=True)

with col2:

    st.markdown('<div class="section-title">System Status</div>',unsafe_allow_html=True)

    if risk_level.lower()=="safe":
        st.success("🟢 Cargo is Safe")

    elif risk_level.lower()=="warning":
        st.warning("🟡 Monitor Cargo")

    else:
        st.error("🔴 Immediate Action Required")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("BioCargo • AI-assisted Cold Chain Monitoring • VMEDITHON 3.0")