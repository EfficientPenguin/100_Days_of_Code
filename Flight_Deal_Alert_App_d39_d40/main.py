'''
    This application retrieves Flight codes and prices from a Google Spreadsheet, checks whether any of the flights
    have a good deal (i.e., less than cost/deal threshold), then sends an email when a deal has been identified.
'''

import os
import json

import requests
import requests_cache
from dotenv import load_dotenv

from FlightData import *
from FlightSearch import *
from DataManager import *

# ----- Load in ENV and apply global cache to reduce Sheety API request quota calls
# Load in .env variables
load_dotenv()

# Cache the response requests
requests_cache.install_cache('global_cache', expire_after=-1)

# ------ Create the objects for the app

# Angel's API only supports the following routes:
#   LHR ⇄ CDG (London Heathrow ↔ Paris Charles de Gaulle)
#   LHR ⇄ FRA (London Heathrow ↔ Frankfurt)
#   LHR ⇄ HND (London Heathrow ↔ Tokyo Haneda)
sheet_manager = DataManager()
flight_data = FlightData(sheet_manager.get_sheet_data())
flight_searcher = FlightSearch()

# Iterate over all Cities To/From LHR
MAIN_CITY = "LHR"
lowest_fare_flights = []

for iataCode in flight_data.data.keys():
    if iataCode != MAIN_CITY:
        # Try MAIN_CITY -> iataCode
        print(f"{MAIN_CITY} -> {iataCode}")
        all_flight_info = flight_searcher.get_flight_and_price_data(MAIN_CITY, iataCode)

        lowest_fare_flights.extend(
            flight_data.get_best_flights_below_lowest_price(all_flight_info=all_flight_info, dst_iata_code=iataCode)
            )

        # Try iataCode -> MAIN_CITY
        print(f"{iataCode} -> {MAIN_CITY}")
        all_flight_info = flight_searcher.get_flight_and_price_data(iataCode, MAIN_CITY)

        lowest_fare_flights.extend(
        flight_data.get_best_flights_below_lowest_price(all_flight_info=all_flight_info, dst_iata_code=MAIN_CITY)
        )

with open(file="flight-all.json", mode='w') as file:
    json.dump(lowest_fare_flights, file, indent=4)

# Print out the flight info in human-readable form
fmtd_flights = flight_data.format_lowest_fare_flights(lowest_fare_flights=lowest_fare_flights)

print(fmtd_flights)

with open(file="fmtd_low_fare_flights.json", mode='w') as file:
    json.dump(fmtd_flights, file, indent=4)
    
    # Get flights from SRC to LHR and LHR to SRC
