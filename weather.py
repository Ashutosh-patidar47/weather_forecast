import requests
from datetime import datetime, timedelta
from dateutil import tz

class WeatherError(Exception):
    pass

# Current weather
def get_current_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    r = requests.get(url)
    if r.status_code != 200:
        raise WeatherError("City not found or API error.")
    
    data = r.json()
    return {
        "city": data["name"],
        "temp": round(data["main"]["temp"]),
        "desc": data["weather"][0]["description"].capitalize(),
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"]
    }

# Next 3 days forecast
def get_daily_forecast(city, api_key, days=4):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    r = requests.get(url)
    if r.status_code != 200:
        raise WeatherError("City not found or API error.")
    
    data = r.json()
    forecast = []
    seen_days = set()

    for entry in data["list"]:
        dt = datetime.utcfromtimestamp(entry["dt"]) + timedelta(hours=data["city"]["timezone"] // 3600)
        day = dt.date()

        if day not in seen_days and len(forecast) < days:
            seen_days.add(day)
            forecast.append({
                "date": dt.strftime("%a, %d %b"),
                "desc": entry["weather"][0]["description"].capitalize(),
                "min": round(entry["main"]["temp_min"]),
                "max": round(entry["main"]["temp_max"])
            })

    return forecast
