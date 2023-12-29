from flask import Flask, render_template, request

from weather_functions import get_current_weather, get_forecast

wetty = Flask(__name__)


@wetty.route("/", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")


@wetty.route("/weather", methods=["GET"])
def get_weather():
    return render_template(
        "weather.html",
        current_weather=get_current_weather("metric"),
        hourly_forecast=get_forecast("metric")[0],
        daily_forecast=get_forecast("metric")[1],
    )


if __name__ == "__main__":
    wetty.run(debug=True)
