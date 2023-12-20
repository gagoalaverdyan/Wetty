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
