'''
    Application to interact with a Google Sheets page to record exercise data for the day. The application
    prompts the user to enter, in natural language, the exercise(s) and the intensity/quantity (e.g., miles ran, heavy weights, etc.).
    Sheety application is linked to my gmail and must have POST and GET enabled for things to work.
'''

import os
import datetime as dt
import requests

# Make sure you export the APP_ID and API_KEY as environment variables before running the script!
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEETY_BASIC_AUTH = f"Basic {os.environ.get("SHEETY_BASIC_AUTH")}"

# Sheety config
sheety_username = "c88e3f99a19f923e6c2ed6ad2b5d9aa8"
sheety_project = "pythonExerciseAppD38"
sheety_exercise_sheet = "sheet1"
sheety_spreadsheet_endpoint = f"https://api.sheety.co/{sheety_username}/{sheety_project}/{sheety_exercise_sheet}"

# NLP Exercise Endpoint
base_api_endpoint = "https://app.100daysofpython.dev"
post_exercise_endpoint = "/v1/nutrition/natural/exercise"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

# Ask for exercise info from user
query = input("What exercises have you done today?: ")

# Set params for the request based on user input
exercise_params = {
    "query": query
}

# Build and send the post request
response = requests.post(url=f"{base_api_endpoint}{post_exercise_endpoint}", json=exercise_params, headers=headers)
response.raise_for_status()

print(response.text)
print(response)

exercise_data = response.json()
exercise_data = exercise_data['exercises'][0]

# Setup POST data for Google Sheets using sheetly endpoint
today = dt.datetime.today()

body = {
    sheety_exercise_sheet: {
        "date": today.strftime("%m/%d/%Y"),
        "time": today.strftime("%H:%M"),
        "exercise": exercise_data['name'],
        "duration": exercise_data['duration_min'],
        "calories": exercise_data['nf_calories']
    } 
}

# Currently have Basic authorization enabled, so we need the authorization header
headers = {
    "Authorization": SHEETY_BASIC_AUTH
}

# Create a new row with the exercise data retrieved from the NLP exercise endpoint
spreadsheet_resp = requests.post(url=sheety_spreadsheet_endpoint, json=body, headers=headers)
print(spreadsheet_resp.text)
print(spreadsheet_resp)
