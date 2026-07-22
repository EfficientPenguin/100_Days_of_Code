'''
    This class is responsible for talking to the Google Sheet via Sheety API.
'''

import os

import requests
import requests_cache
from dotenv import load_dotenv

# Load in .env variables
load_dotenv()

# Constants
SHEET_AUTH = f"Basic {os.getenv("SHEETY_AUTH")}"
BASE_ENDPOINT = os.getenv("SHEETY_BASE_ENDPOINT")
USERNAME = os.getenv("SHEETY_USERNAME")
PROJECT = os.getenv("SHEETY_PROJECT")
SHEET = os.getenv("SHEETY_SHEET")
SHEETY_API_ENDPOINT = f"{BASE_ENDPOINT}{USERNAME}/{PROJECT}/{SHEET}"

class DataManager:
    def __init__(self):
        self.headers = {
            "Authorization": SHEET_AUTH
        }
        self.post_params = self.init_post_params()
    
    def init_post_params(self) -> dict:
        ''' Function to initialize the POST parameters needed for a request call.'''
        post_params = {
            SHEET: {
                "city": "",
                "iataCode": "",
                "lowestPrice": ""
            }
        }

        return post_params
    
    def get_sheet_data(self) -> dict:
        ''' Function to get all data (i.e., all rows) from the designated spreadsheet.'''
        response = requests.get(url=SHEETY_API_ENDPOINT, headers=self.headers)
        print(f"Using cached sheet data: {response.from_cache}")

        return response.json()[SHEET]

if __name__ == "__main__":
    my_manager = DataManager()