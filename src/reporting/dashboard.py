import sys
import os

import streamlit as st
import pandas as pd
from src.agents.power_engineering import PowerEngineeringAgent
from src.agents.climate_mrv import ClimateMRVAgent
from src.agents.adaptation_risk import AdaptationRiskAgent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.set_page_config(
    page_title="UNIDO Cleantech MRV Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 UNIDO Cleantech dMRV Engine")
st.caption("Multi-Agent Industrial Decarbonization & Climate Adaptation Analytics (GCIP / CTCN / GEF Alignment)")

# Sidebar Controls
st.sidebar.header("Industrial Telemetry Parameters")
device_id = st.sidebar.text_input("Device ID", "DEV-MSME-001")
voltage = st.sidebar.slider("Line Voltage (V)", 300.0, 480.0, 400.0)
current = st.sidebar.slider("Phase Current (A)", 10.0, 500.0, 120.0)
power_factor = st.sidebar.slider("Power Factor", 0.50, 0.99, 0.82)
ambient_temp = st.sidebar.slider("Ambient Temp (°C)", 20.0, 55.0, 42.0)
vfd_installed = st.sidebar.checkbox("VFD System Installed", value=True)

st.sidebar.header("Baseline vs Project Energy")
baseline_kwh = st.sidebar.number_input("Baseline Annual Consumption (kWh)", value=315000.0)
project_kwh = st.sidebar.number_input("Project Annual Consumption (kWh)", value=220500.0)
refrigerant_saved = st.sidebar.number_input("Avoided Refrigerant Leakage (kg)", value=12.5)

# Initialize Agents
power_agent = PowerEngineeringAgent()
mrv_agent = ClimateMRVAgent()
adaptation_agent = AdaptationRiskAgent()

# Run Analytics
telemetry = {
    "voltage_v": voltage,
    "current_a": current,
    "power_factor": power_factor,
    "vfd_installed": vfd_installed,
    "operating_hours": 4200
}

power_res = power_agent.analyze_efficiency(telemetry)
mrv_res = mrv_agent.compute_avoided_emissions(baseline_kwh, project_kwh, refrigerant_saved)
adaptation_res = adaptation_agent.assess_thermal_vulnerability(ambient_temp)

# Top Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Power", f"{power_res['active_power_kw']} kW")
col2.metric("Avoided Emissions", f"{mrv_res['total_avoided_tco2e']} tCO2e/yr")
col3.metric("GEF Core Indicator 6.2", f"{mrv_res['gef_indicator_6_2_tco2e']} tCO2e")
col4.metric("Climate Risk Score", f"{adaptation_res['climate_risk_score']} / 10")

st.divider()




# Detailed Breakdowns
tab1, tab2, tab3 = st.tabs(["⚡ Power Systems Analytics", "🌍 Climate MRV & Finance", "🔥 Thermal Risk & Resilience"])

with tab1:
    st.subheader("ISO 50001 / IEC 60204 Electrical Performance")
    p_df = pd.DataFrame([power_res]).T.rename(columns={0: "Metric Value"}).astype(str)
    st.table(p_df)

with tab2:
    st.subheader("IEEE P7802 Greenhouse Gas Reduction Tracking")
    m_df = pd.DataFrame([mrv_res]).T.rename(columns={0: "Value"}).astype(str)
    st.table(m_df)

with tab3:
    st.subheader("Adaptation Vulnerability & Equipment Derating")
    a_df = pd.DataFrame([adaptation_res]).T.rename(columns={0: "Assessment"}).astype(str)
    st.table(a_df)


