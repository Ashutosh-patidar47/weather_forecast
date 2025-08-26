import os
import streamlit as st
import requests
import smtplib
from datetime import datetime

# -----------------------------------
# 🔑 Load secrets from Streamlit Cloud
# -----------------------------------
OWM_KEY = st.Secrets["WEATHER_API_KEY"]      # OpenWeatherMap API Key
SENDER = st.Secrets["EMAIL_ADDRESS"]         # Sender Email
PASSWORD = st.Secrets["EMAIL_PASSWORD"]      # Gmail App Password
SMTP = "smtp.gmail.com"
PORT = 587

# -----------------------------------
# 🌤️ Fetch weather from OpenWeatherMap
# -----------------------------------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OWM_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# -----------------------------------
# 📩 Send weather report via email
# -----------------------------------
def send_email(receiver, subject, body):
    try:
        with smtplib.SMTP(SMTP, PORT) as server:
            server.starttls()
            server.login(SENDER, PASSWORD)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(SENDER, receiver, message)
        return True
    except Exception as e:
        return str(e)

# -----------------------------------
# 🎨 Streamlit UI
# -----------------------------------
st.set_page_config(page_title="Weather Forecast", page_icon="⛅", layout="centered")

st.title("🌦 Weather Forecast App")
st.write("Get the current weather and a 3-day forecast. Optionally receive the report by email.")

city = st.text_input("🏙 Enter City Name:")
email = st.text_input("📧 Enter Email (optional, to receive forecast):")

if st.button("Get Forecast"):
    if not city:
        st.error("⚠️ Please enter a city name.")
    else:
        data = get_weather(city)

        if data and "list" in data:
            # ✅ Current weather
            today = data["list"][0]
            temp = today["main"]["temp"]
            desc = today["weather"][0]["description"].title()
            humidity = today["main"]["humidity"]
            wind = today["wind"]["speed"]

            st.subheader(f"🌞 Current Weather in {city.title()}")
            st.write(f"**{temp}°C** • {desc}")
            st.write(f"💧 Humidity: {humidity}% • 🌬 Wind: {wind} m/s")

            # ✅ 3-day forecast
            st.subheader("📅 3-Day Forecast")
            forecast_data = {}
            for item in data["list"]:
                date = datetime.fromtimestamp(item["dt"]).strftime("%a, %d %b")
                if date not in forecast_data:
                    forecast_data[date] = {
                        "temp_min": item["main"]["temp_min"],
                        "temp_max": item["main"]["temp_max"],
                        "condition": item["weather"][0]["description"].title()
                    }

            days = list(forecast_data.items())[:3]
            for date, info in days:
                st.markdown(f"""
                    <div style="
                        background-color:#1c1f26;
                        border-radius:12px;
                        padding:12px;
                        margin-bottom:12px;
                        box-shadow:0 4px 10px rgba(0,0,0,0.4);
                        color:#f8fafc;">
                        <b style="color:#38bdf8;">{date}</b><br>
                        🌤 {info['condition']}<br>
                        🌡 <span style="color:#ef4444;">Max: {info['temp_max']}°C</span> |
                        <span style="color:#22d3ee;">Min: {info['temp_min']}°C</span>
                    </div>
                """, unsafe_allow_html=True)

            # ✅ Send email if email provided
            if email:
                report = f"Weather Report for {city}\n\nCurrent: {desc}, {temp}°C\nHumidity: {humidity}%\nWind: {wind} m/s\n\nForecast:\n"
                for date, info in days:
                    report += f"{date}: {info['condition']} ({info['temp_min']}°C - {info['temp_max']}°C)\n"

                status = send_email(email, f"Weather Update for {city}", report)
                if status is True:
                    st.success("📩 Email Sent Successfully!")
                else:
                    st.error(f"❌ Failed to send email: {status}")
        else:
            st.error("City not found. Please try again.")


