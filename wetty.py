import requests
from flask import Flask, render_template, request

from weather_functions import get_current_weather, get_forecast

wetty = Flask(__name__)


@wetty.route("/", methods=["GET"])
def search():
    if request.method == "GET":
        popular_cities = [
            "Yerevan",
            "Los Angeles",
            "Moscow",
            "Delhi",
            "Reykjavík",
            "Santiago",
            "Berlin",
            "Rome",
            "Toronto",
            "Prague",
            "Paris",
            "Seoul",
            "Barcelona",
            "Lima",
        ]
        return render_template(
            "search.html",
            cities=popular_cities,
        )


@wetty.route("/weather", methods=["GET"])
def get_weather():
    if request.method == "GET":
        city = request.args.get("city")
        units = request.args.get("units").lower()
        api_key = "ba9df5150897844664a1f1a0616be528"
        weather_request_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={api_key}"
        forecast_request_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={api_key}"
        weather_json = requests.get(weather_request_url).json()
        forecast_json = requests.get(forecast_request_url).json()

        try:
            current_weather_dict = get_current_weather(weather_json, units)
            forecast_tuple = get_forecast(forecast_json, units)
            return render_template(
                "weather.html",
                current_weather=current_weather_dict,
                hourly_forecast=forecast_tuple[0],
                daily_forecast=forecast_tuple[1],
            )
        except:
            return render_template("error.html")


if __name__ == "__main__":
    wetty.run(debug=True)
