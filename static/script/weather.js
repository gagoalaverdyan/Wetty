function updateWeatherBackground() {
    var weatherCondition = document.getElementById("weather-state-text").innerText;
    var weatherBackground = document.getElementById("current-weather");
    const atmosphereConditions = ['Mist', "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash", "Squall", "Tornado"]

    if (atmosphereConditions.includes(weatherCondition)) {
        weatherBackground.style.backgroundImage = "url(static/images/weather-backgrounds/mist.png)"
    } else {
        weatherBackground.style.backgroundImage = `url(static/images/weather-backgrounds/${weatherCondition.toLowerCase()}.png)`
    }
}

function updateAqiBackground() {
    var aqiPoint = document.getElementById("current-aqi-point").innerText;
    var aqiBackground = document.getElementById("current-air-quality")
    console.log(aqiPoint)
    if (aqiPoint === "1" | aqiPoint === "2") {
        aqiBackground.style.backgroundImage = "url(static/images/aqi/good.png)"
    } else if (aqiPoint === "3") {
        aqiBackground.style.backgroundImage = "url(static/images/aqi/moderate.png)"
    } else if (aqiPoint === "4" | aqiPoint === "5") {
        aqiBackground.style.backgroundImage = "url(static/images/aqi/poor.png)"
    }
}

updateWeatherBackground()
updateAqiBackground()