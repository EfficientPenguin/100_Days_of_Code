'''
    This application pulls weather data from the openweathermap.org weather API and sends
    an SMS message to my cell phone.
'''
import os
import json

import requests


api_key = os.environ.get("API-KEY")
weather_url = "https://api.openweathermap.org/data/2.5/forecast"
city = "San Francisco"
state = "US-CA"
country_code = "US"

params = {
    'lat': 37.7749,
    'lon': -122.4194,
    'cnt': 4,
    'appid': api_key
}

url = f"{weather_url}?q={city},{state},{country_code}&appid={api_key}"

# Make a request to the URL
response = requests.get(url=weather_url, params=params)
response.raise_for_status()

data = response.json()

with open(file='weather.json', mode='w') as file:
    json.dump(data, file, indent=4)

# Check if it's going to rain in the next 12 hours (i.e., cnt=4)
for weather in data['list']:
    if int(weather['weather'][0]['id']) < 800:
        print(f'Bring an umbrella on {weather['weather']['dt_txt']}')
    print(weather['weather'][0])

# Print out HTTP response code, and the response itself (only weather id and description)
# print(data)
# print(data['weather'][0]['id'])
# print(data['weather'][0]['description'])
