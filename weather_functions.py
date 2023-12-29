import json
from datetime import datetime

import requests
from flask import url_for


# Integrate the API, update api keys to variables
def get_weather_icon(condition):
    """Returns weather icon based on condition or returns mist for atmosphere conditions."""
    filenames = {
        "Clear": "images/weather/clear.png",
        "Thunderstorm": "images/weather/thunderstorm.png",
        "Drizzle": "images/weather/drizzle.png",
        "Rain": "images/weather/rain.png",
        "Snow": "images/weather/snow.png",
        "Clouds": "images/weather/clouds.png",
    }
    if condition in filenames.keys():
        return filenames[condition]
    else:
        return "images/weather/mist.png"


# Needs to get city, units, api key in future
def get_current_weather(units):
    """Returns a dictionary of current weather information"""

    def get_hours_minutes(delta1, delta2):
        """Returns difference between to timedelta objects in hours and minutes."""
        difference_delta = delta1 - delta2
        hours, rem = divmod(difference_delta.seconds, 3600)
        minutes, _ = divmod(rem, 60)
        return f"{hours}h {minutes}m"

    def get_wind_direction(degree):
        """Returns the wind direction based on the wind degree."""
        directions = [
            "N",
            "NNE",
            "NE",
            "ENE",
            "E",
            "ESE",
            "SE",
            "SSE",
            "S",
            "SSW",
            "SW",
            "WSW",
            "W",
            "WNW",
            "NW",
            "NNW",
        ]
        i = round(degree / (360.0 / len(directions))) % len(directions)
        return directions[i]

    def get_current_aqi(lat, lon, api_key):
        """Returns a dictionary of AQI info from OpenWeatherMap, given location's lat and lon."""
        request_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        aqi_json = requests.get(request_url).json()
        aqi_dict = dict()
        options = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        aqi_dict["point"] = aqi_json["list"][0]["main"]["aqi"]
        aqi_dict["text"] = options[aqi_dict["point"]]
        return aqi_dict

    def get_weather_background(condition):
        """Returns weather background based on condition or returns mist for atmosphere conditions."""
        filenames = {
            "Clear": "images/weather_backgrounds/clear.png",
            "Thunderstorm": "images/weather_backgrounds/thunderstorm.png",
            "Drizzle": "images/weather_backgrounds/drizzle.png",
            "Rain": "images/weather_backgrounds/rain.png",
            "Snow": "images/weather_backgrounds/snow.png",
            "Clouds": "images/weather_backgrounds/clouds.png",
        }
        if condition in filenames.keys():
            return filenames[condition]
        else:
            return "images/weather_backgrounds/mist.png"

    # Using a local copy of OpenWeather JSON for Yerevan's weather
    with open("current_json.json", "r", encoding="utf-8") as fp:
        weather_json = json.load(fp)

    # Turning sunrise and sunset times into datetime objects
    sunrise_raw = datetime.fromtimestamp(int(weather_json["sys"]["sunrise"]))
    sunset_raw = datetime.fromtimestamp(int(weather_json["sys"]["sunset"]))

    # Getting the requested location's AQI
    location_lat = weather_json["coord"]["lat"]
    location_lon = weather_json["coord"]["lon"]
    aqi_dict = get_current_aqi(
        location_lat, location_lon, "ba9df5150897844664a1f1a0616be528"
    )

    # Initiating the current weather dictionary's universal elements
    current_weather = {
        "city": weather_json["name"],
        "condition": weather_json["weather"][0]["main"],
        "icon": url_for(
            "static", filename=get_weather_icon(weather_json["weather"][0]["main"])
        ),
        "background": url_for(
            "static",
            filename=get_weather_background(weather_json["weather"][0]["main"]),
        ),
        "humidity": str(round(weather_json["main"]["humidity"])) + "%",
        "daytime": get_hours_minutes(sunset_raw, sunrise_raw),
        "cloudiness": str(weather_json["clouds"]["all"]) + "%",
        "wind_deg": get_wind_direction(weather_json["wind"]["deg"]),
        "aqi_point": aqi_dict["point"],
        "aqi_text": aqi_dict["text"],
    }

    # Initiating the remaing elements based on the unit choice
    if units == "metric":
        current_weather["time"] = datetime.fromtimestamp(
            int(weather_json["dt"])
        ).strftime("%H:%M, %d %b, %a")
        current_weather["temp"] = str(round(weather_json["main"]["temp"])) + "°C"
        current_weather["feels_like"] = (
            str(round(weather_json["main"]["feels_like"])) + "°C"
        )
        current_weather["pressure"] = (
            str(round(weather_json["main"]["pressure"])) + " mb"
        )
        current_weather["visibility"] = (
            str(round(weather_json["visibility"] / 1000, 1)) + " km"
        )
        current_weather["sunrise"] = sunrise_raw.strftime("%H:%M")
        current_weather["sunset"] = sunset_raw.strftime("%H:%M")
        current_weather["wind_speed"] = (
            str(round(weather_json["wind"]["speed"], 1)) + " km/h"
        )
    elif units == "imperial":
        current_weather["time"] = datetime.fromtimestamp(
            int(weather_json["dt"])
        ).strftime("%I:%M %p, %d %b, %a")
        current_weather["temp"] = str(round(weather_json["main"]["temp"])) + "°F"
        current_weather["feels_like"] = (
            str(round(weather_json["main"]["feels_like"])) + "°F"
        )
        current_weather["pressure"] = (
            str(round(weather_json["main"]["pressure"]) * 0.0145038) + " Pa"
        )
        current_weather["visibility"] = (
            str(round(weather_json["visibility"] * 0.000621371, 1)) + " mi"
        )
        current_weather["sunrise"] = sunrise_raw.strftime("%I:%M %p")
        current_weather["sunset"] = sunset_raw.strftime("%I:%M %p")
        current_weather["wind_speed"] = (
            str(round(weather_json["wind"]["speed"] * 0.000621371, 1)) + " km/h"
        )

    return current_weather


# Needs to get city, units, api key in future
def get_forecast(units):
    """Returns daily and hourly forecast dictionaries."""
    # Getting the OpenWeatherMap JSON and processing required values
    with open("forecast_json.json", "r", encoding="utf-8") as fp:
        forecast_json = json.load(fp)

    raw_forecast = dict()
    for elem in forecast_json["list"]:
        raw_forecast[elem["dt"]] = {
            "temp": elem["main"]["temp"],
            "main": elem["weather"][0]["main"].title(),
        }

    # Initiating temporary dictionaries
    daily_forecast_temp = dict()
    daily_state_temp = dict()

    # Initiating the target dictionaries
    daily_forecast = dict()
    hourly_forecast = dict()

    for date, content in raw_forecast.items():
        date_from_utc = datetime.fromtimestamp(int(date))

        # Getting the daily forecast values in a temp dictionary
        date_part = date_from_utc.strftime("%d %b")
        if date_part not in daily_forecast_temp:
            daily_forecast_temp[date_part] = [
                int(content["temp"]),
            ]
        else:
            daily_forecast_temp[date_part].append(int(content["temp"]))

        # Getting the daily state values in a temp dictionary
        if date_part not in daily_state_temp:
            daily_state_temp[date_part] = [
                content["main"],
            ]
        else:
            daily_state_temp[date_part].append(content["main"])

        # Getting the hourly forecast based on units choice
        if units == "metric":
            hourly_time = date_from_utc.strftime("%H:%M")
            if date_part not in hourly_forecast.keys():
                hourly_forecast[date_part] = [
                    {
                        "time": hourly_time,
                        "temp": str(round(content["temp"])) + "°C",
                        "state": content["main"].title(),
                        "icon": url_for(
                            "static", filename=get_weather_icon(content["main"].title())
                        ),
                    }
                ]
            else:
                hourly_forecast[date_part].append(
                    {
                        "time": hourly_time,
                        "temp": str(round(content["temp"])) + "°C",
                        "state": content["main"].title(),
                        "icon": url_for(
                            "static", filename=get_weather_icon(content["main"].title())
                        ),
                    }
                )
        elif units == "imperial":
            hourly_time = date_from_utc.strftime("%I:%M %p")
            if date_part not in hourly_forecast.keys():
                hourly_forecast[date_part] = [
                    {
                        "time": hourly_time,
                        "temp": str(round(content["temp"])) + "°F",
                        "state": content["main"].title(),
                        "icon": url_for(
                            "static", filename=get_weather_icon(content["main"].title())
                        ),
                    }
                ]
            else:
                hourly_forecast[date_part].append(
                    {
                        "time": hourly_time,
                        "temp": str(round(content["temp"])) + "°F",
                        "state": content["main"].title(),
                        "icon": url_for(
                            "static", filename=get_weather_icon(content["main"].title())
                        ),
                    }
                )

    # Processing the temporary daily values and getting the min and max based on units
    if len(daily_forecast_temp) == 6:
        del daily_forecast_temp[next(iter(daily_forecast_temp))]
        del daily_state_temp[next(iter(daily_state_temp))]
    for date, values in daily_forecast_temp.items():
        min_value = min(values)
        max_value = max(values)
        if units == "metric":
            daily_forecast[date] = {
                "min": str(min_value) + "°C",
                "max": str(max_value) + "°C",
                "state": daily_state_temp[date][4],
            }
        elif units == "imperial":
            daily_forecast[date] = {
                "min": str(min_value) + "°C",
                "max": str(max_value) + "°F",
                "state": daily_state_temp[date][4],
            }
    return (hourly_forecast, daily_forecast)


if __name__ == "__main__":
    print("Nothing to launch here. The server is run via wetty.py")
