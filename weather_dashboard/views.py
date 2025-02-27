import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime

def get_weather_data(city):
    api_key = settings.OPENWEATHER_API_KEY
    base_url = "https://api.openweathermap.org/data/2.5/"

    # API URLs
    weather_url = f"{base_url}weather?q={city}&appid={api_key}&units=metric"
    forecast_url = f"{base_url}forecast?q={city}&appid={api_key}&units=metric"

    weather_response = requests.get(weather_url).json()
    forecast_response = requests.get(forecast_url).json()

    if weather_response.get("cod") != 200:
        return None, None

    daily_forecast = {}
    for item in forecast_response.get("list", []):
        date = item["dt_txt"].split(" ")[0]
        time = item["dt_txt"].split(" ")[1]

        
        if date not in daily_forecast or time == "12:00:00":
            daily_forecast[date] = item

    
    filtered_forecast = list(daily_forecast.values())

    return weather_response, filtered_forecast

def weather_dashboard(request):
    city = request.GET.get("city", "")
    weather_data, forecast_data = None, None

    if city:
        weather_data, forecast_data = get_weather_data(city)

    return render(request, "weather_dashboard.html", {
        "weather": weather_data,
        "forecast": forecast_data,
        "city": city
    })
