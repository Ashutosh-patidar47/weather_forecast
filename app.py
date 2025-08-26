import streamlit as st
from weather import get_current_weather, get_daily_forecast, WeatherError
from emailer import render_html, send_email

# Page config
st.set_page_config(page_title="Weather Email Service", page_icon="🌤️", layout="centered")

# Custom CSS with premium color scheme
st.markdown("""
    <style>
        body {
            background-color: #0d1117;
            color: #e5e5e5;
        }
        .title {
            font-size: 30px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        .subtitle {
            font-size: 22px;
            font-weight: 600;
            margin-top: 25px;
            margin-bottom: 10px;
        }
        .weather-box {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            color: #f8fafc;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .forecast-card {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border-radius: 15px;
            padding: 18px;
            margin-bottom: 20px;
            color: #f8fafc;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            transition: transform 0.2s ease-in-out;
        }
        .forecast-card:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(0,0,0,0.6);
        }
        .forecast-date {
            font-weight: 700;
            font-size: 18px;
            color: #38bdf8;  /* sky blue */
            margin-bottom: 8px;
        }
        .forecast-condition {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .forecast-condition.sunny { color: #facc15; }   /* yellow */
        .forecast-condition.rain { color: #3b82f6; }    /* blue */
        .forecast-condition.cloud { color: #9ca3af; }   /* gray */
        .forecast-temp {
            font-size: 16px;
            font-weight: 600;
        }
        .forecast-temp span.max { color: #ef4444; }   /* red */
        .forecast-temp span.min { color: #22d3ee; }   /* cyan */
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 class='main-title'>🌤️ Weather Forecast Email Service</h1>", unsafe_allow_html=True)

# Secrets (replace with your actual)
OWM_KEY = "60d975cfef77aedca8bab27b843bafb6"
SENDER = "your email id"
PASSWORD = "generated app password"
SMTP = "smtp.gmail.com"
PORT = 587

# Input form
with st.form("weather_form"):
    city = st.text_input("🏙️ Enter City", placeholder="e.g. London")
    email = st.text_input("📧 Enter Email", placeholder="e.g. user@example.com")
    submitted = st.form_submit_button("Get Forecast & Send Email")

if submitted:
    try:
        # Get weather
        current = get_current_weather(city, OWM_KEY)
        forecast = get_daily_forecast(city, OWM_KEY, days=4)  # today + 3 days

        # Current weather card
        st.markdown(f"""
        <div class="weather-card">
            <h3>☀️ Current Weather in {current['city']}</h3>
            <p><b>{current['temp']}°C</b> · {current['desc']}</p>
            <p>💧 Humidity: {current['humidity']}% · 🌬️ Wind: {current['wind']} m/s</p>
        </div>
        """, unsafe_allow_html=True)

        # Forecast cards
        st.subheader("📅 3-Day Forecast")
        for d in forecast:
            st.markdown(f"""
            <div class="weather-card">
                <p class="forecast-date">{d['date']}</p>
                <p>{d['desc']} | 🌡️ {d['min']}°C – {d['max']}°C</p>
            </div>
            """, unsafe_allow_html=True)

        # Send email
        html_body = render_html(current["city"], current, forecast)
        text_body = f"Weather in {current['city']} Now: {current['temp']}°C · {current['desc']}"
        send_email(email, f"Weather Forecast for {current['city']}", html_body, text_body, SENDER, PASSWORD, SMTP, PORT)

        st.success(f"📩 Email sent successfully to {email}")

    except WeatherError as we:
        st.error(str(we))
    except Exception as e:
        st.error(f"Error: {e}")
