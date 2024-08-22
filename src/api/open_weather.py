import requests
import pandas as pd


def get_weather_forecast(latitude: float, longitude: float, start_time: str, end_time: str):
    """
    Get the weather forecast for the next 3 days. The forecast are acquired from the open-source API of https://open-meteo.com.
    The variables retrieved are: air temperature, wind speed, shortwave radiation, diffuse radiation and direct normal irradiance.
    :return:
    """

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,wind_speed_10m,shortwave_radiation,diffuse_radiation,direct_normal_irradiance&start_hour={start_time}&end_hour={end_time}&timezone=Europe%2FLondon"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()["hourly"]
    data = pd.DataFrame(data)
    data.columns = ["timestamp", "temp_air", "wind_speed", "ghi", "dhi", "dni"]

    return data


if __name__ == "__main__":
    import json
    import datetime

    # Load config.json
    with open("../../config.json", "r") as f:
        config = json.load(f)

    latitude = config["latitude"]
    longitude = config["longitude"]

    start_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    end_time = start_time + datetime.timedelta(days=1)

    start_hour = start_time.strftime("%Y-%m-%dT%H:%M")
    end_hour = end_time.strftime("%Y-%m-%dT%H:%M")

    data = get_weather_forecast(latitude, longitude, start_hour, end_hour)
    print(data)