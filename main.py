from dotenv import dotenv_values

import requests
from twilio.rest import Client

config = dotenv_values(".env")

ACCOUNT_SID = config["ACCOUNT_SID"]
AUTH_TOKEN = config["AUTH_TOKEN"]
FROM_PHONE_NUMBER = config["FROM_PHONE_NUMBER"]
TO_PHONE_NUMBER = config["TO_PHONE_NUMBER"]
OWM_APP_ID = config["OWM_APP_ID"]
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"

LAT = config["MY_LAT"]
LONG = config["MY_LONG"]

print(LAT, LONG)
params = {
    "appid": OWM_APP_ID,
    "lat": LAT,
    "lon": LONG,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_ENDPOINT, params=params)
response.raise_for_status()

data = response.json()
# Get forecast for next 12 hours
hourly_forecast = data["hourly"][:12]
# Isolate the weather object that we are interested in
hourly_forecast_weather = [item["weather"][0] for item in hourly_forecast]
# Filter forecasts by rain forecasts
rain_forecasts = [forecast for forecast in hourly_forecast_weather if forecast["id"] < 700]

if len(rain_forecasts):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages \
        .create(
            body="It's likely to rain ☔️!",
            from_=FROM_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
    print(message.status)