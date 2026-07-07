import streamlit as st
import pandas as pd
import time
import random

# Page configuration
st.set_page_config(
    page_title="Phyfarm Smart Agriculture Dashboard",
    page_icon="🌱",
    layout="wide"
)

# Title
st.title("🌱 Phyfarm IoT Monitoring Dashboard")
st.markdown("Real-time tracking of hydroponic and agricultural sensor data.")

# Sidebar for controls
st.sidebar.header("System Controls")
pump_status = st.sidebar.toggle("Water Pump Switch", value=False)

if pump_status:
    st.sidebar.success("💦 Pump is currently RUNNING")
else:
    st.sidebar.error("❌ Pump is currently OFF")

# Simulating real-time data fetching
def get_sensor_data():
    # In a real project, replace this with your API call or MQTT subscriber
    return {
        "temperature": round(random.uniform(22.0, 28.0), 1),
        "humidity": round(random.uniform(50.0, 70.0), 1),
        "ph_level": round(random.uniform(5.5, 6.5), 2),
        "ec_level": round(random.uniform(1.2, 2.0), 2)
    }

# Create dashboard layout using metrics
data = get_sensor_data()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Temperature (°C)", value=f"{data['temperature']} °C", delta="Normal")

with col2:
    st.metric(label="Humidity (%)", value=f"{data['humidity']} %", delta="-1%")

with col3:
    st.metric(label="pH Level", value=data['ph_level'], delta="Optimal")

with col4:
    st.metric(label="EC Level (mS/cm)", value=data['ec_level'])

---

# Live Data Chart Simulation
st.subheader("📈 Real-time Parameter Trends")

# Initialize historical data in session state if it doesn't exist
if "df_history" not in st.session_state:
    st.session_state.df_history = pd.DataFrame(columns=["Time", "pH", "Temp"])

# Simulation loop to mimic live updates
placeholder = st.empty()

for i in range(10):
    current_time = time.strftime("%H:%M:%S")
    new_data = get_sensor_data()
    
    # Append new row using pd.concat
    new_row = pd.DataFrame([{"Time": current_time, "pH": new_data["ph_level"], "Temp": new_data["temperature"]}])
    st.session_state.df_history = pd.concat([st.session_state.df_history, new_row], ignore_index=True)
    
    with placeholder.container():
        st.line_chart(st.session_state.df_history.set_index("Time"))
    
    time.sleep(2)

