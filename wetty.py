from datetime import datetime

import requests
from flask import Flask, jsonify, render_template

wetty = Flask(__name__)


@wetty.route("/")
def hello_world():
    return render_template("search.html")


@wetty.route("/search", methods=["GET"])
def get_weather():
    api_key = "ba9df5150897844664a1f1a0616be528"
    city = "Yerevan"
    units = "metric"
    request_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={api_key}"
    # weather_json = requests.get(request_url).json()
    # current_weather_dict = {
    #     "city": weather_json["name"],
    #     "current_weather": weather_json["main"]["temp"],
    # }
    current_weather_dict = {
        "city": "Yerevan",
        "current_weather": "10",
    }
    return render_template("weather.html", context=current_weather_dict)


if __name__ == "__main__":
    wetty.run(debug=True)


def get_forecast(city, units, api_key):
    # Getting the raw info from OpenWeather API
    request_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={api_key}"
    weather_json = requests.get(request_url).json()
    raw_forecast = dict()
    for elem in weather_json["list"]:
        raw_forecast[elem["dt"]] = {
            "temp": elem["main"]["temp"],
            "main": elem["weather"][0]["description"],
        }

    daily_forecast = dict()
    hourly_forecast = dict()

    for date, content in raw_forecast.items():
        date_from_utc = datetime.fromtimestamp(int(date))
        # Getting the daily forecast
        date_part = date_from_utc.strftime("%d %b")
        if date_part not in daily_forecast:
            daily_forecast[date_part] = {
                "min": int(content["temp"]),
                "max": int(content["temp"]),
            }
        else:
            daily_forecast[date_part]["min"] = min(
                daily_forecast[date_part]["min"], int(content["temp"])
            )
            daily_forecast[date_part]["max"] = max(
                daily_forecast[date_part]["max"], int(content["temp"])
            )
        # Getting the hourly forecast
        hourly_time = date_from_utc.strftime("%H:%M")
        if date_part not in hourly_forecast.keys():
            hourly_forecast[date_part] = [
                {"time": hourly_time, "temp": int(content["temp"])}
            ]
        else:
            hourly_forecast[date_part].append(
                {"time": hourly_time, "temp": int(content["temp"])}
            )
    return (hourly_forecast, daily_forecast)
