import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from src.pipeline.orchestrator import run_pipeline

load_dotenv()

# -------- DATA --------
def get_hamburg_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 53.5511,
        "longitude": 9.9937,
        "current": ["temperature_2m", "wind_speed_10m"]
    }
    return requests.get(url, params=params).json()["current"]

def get_mock_ship_data():
    return [
        {"name": "HMM Oslo", "status": "arriving", "eta_hours": 3},
        {"name": "Ever Given II", "status": "anchored", "eta_hours": 12},
        {"name": "Maersk Antwerp", "status": "departed", "eta_hours": 6},
    ]

def build_context(weather, ships):
    return {"weather": weather, "ships": ships}


# -------- UI --------
st.title("🚢 HavenAI — Hamburg Logistics Dashboard")

if st.button("Run Analysis"):
    weather = get_hamburg_weather()
    ships = get_mock_ship_data()
    context = build_context(weather, ships)

    st.subheader("🌦 Current Conditions (Hamburg Port)")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Temperature (°C)", weather["temperature_2m"])
    with col2:
        st.metric("Wind Speed (km/h)", weather["wind_speed_10m"])


    st.subheader("🚢 Active Shipments")
    df = pd.DataFrame(ships)
    st.dataframe(df)

    with st.spinner("Analyzing logistics risk..."):
        result = run_pipeline(context)

    st.subheader("🤖 AI Risk Analysis")
    st.markdown(f"""
    <div style="background-color:#303234;padding:15px;border-radius:10px">
    {result}
    </div>
    """, unsafe_allow_html=True)