'''
    This class is responsible for talking to the Flight Search API.
'''

import os
import datetime as dt
import json

import requests
import requests_cache
from dotenv import load_dotenv

# Load in .env variables
load_dotenv()

# Constants
X_APP_ID = os.getenv("X_APP_ID")
X_API_KEY = os.getenv("X_API_KEY")
FLIGHT_BASE_ENDPOINT = os.getenv("FLIGHT_BASE_ENDPOINT")
FLIGHT_GET_REQUEST = os.getenv("FLIGHT_GET_REQUEST")

DATE_FMT = "%Y-%m-%d"

class FlightSearch:
    def __init__(self):
        pass

    def get_flight_and_price_data(self, dep: str, arr: str) -> dict:
        ''' Function to make GET request that returns the flight and price data for single city.'''

        # Set outbound date to today, and return 7 days after
        outbound_date = dt.datetime.today()
        return_date = outbound_date + dt.timedelta(days=7)

        # Assume 1 adult, one-way tickets only
        params = {
            "engine": "google_flights",
            "api_key": X_API_KEY,
            "departure_id": dep,
            "arrival_id": arr,
            "outbound_date": outbound_date.strftime(DATE_FMT),
            "return_date": return_date.strftime(DATE_FMT),
            "type": 2           # 1 = round trip, 2 = one way
        }

        # Send the GET request
        response = requests.get(url=f"{FLIGHT_BASE_ENDPOINT}{FLIGHT_GET_REQUEST}", params=params)
        response.raise_for_status()
        
        # with open(file="flight-search.json", mode="w") as file:
        #     json.dump(response.json(), file, indent=4)
        
        return response.json()

if __name__ == "__main__":
    flight_search = FlightSearch()
    best_flights = flight_search.get_flight_and_price_data('LHR', 'CDG')

    for flight in best_flights:
        print(flight['price'])
