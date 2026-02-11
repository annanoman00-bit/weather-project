import streamlit as st
import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Load env
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Page config
st.set_page_config(
    page_title="Weather Forecast App",
    page_icon="🌤️",
    layout="centered"
)

st.title("🌍 Weather Forecast App")
st.markdown("Simple • Clean • Powerful")

city = st.text_input("🏙️ Enter City Name")

# ---------- CURRENT WEATHER ----------
def current_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

# ---------- FORECAST ----------
def forecast_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

if st.button("🔍 Get Weather"):
    if not city:
        st.warning("Please enter a city name")
    else:
        data = current_weather(city)

        if data.get("cod") != 200:
            st.error("City not found ❌")
        else:
            # Current weather
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"].title()
            icon = data["weather"][0]["icon"]

            st.subheader("📍 Current Weather")
            col1, col2 = st.columns(2)

            with col1:
                st.metric("🌡️ Temperature", f"{temp} °C")
                st.metric("💧 Humidity", f"{humidity}%")

            with col2:
                st.metric("🤗 Feels Like", f"{feels} °C")
                st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png")

            st.info(f"☁️ Condition: *{desc}*")

            # Forecast
            st.subheader("📊 5-Day Forecast (Every 3 Hours)")
            forecast = forecast_weather(city)

            forecast_list = forecast["list"]
            temps = []
            times = []

            for item in forecast_list[:15]:
                temps.append(item["main"]["temp"])
                times.append(item["dt_txt"])

            df = pd.DataFrame({
                "Time": times,
                "Temperature (°C)": temps
            })

            st.line_chart(df.set_index("Time"))

            st.success("✅ Data loaded successfully")