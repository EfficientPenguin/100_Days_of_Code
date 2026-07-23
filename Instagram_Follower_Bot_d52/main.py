'''
    This application uses Selenium to automatically follow people on Instagram or the test site made by Dr. Angela Yu.
'''

import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from InstaFollower import InstaFollower

# Load in the .env variables
load_dotenv()

# Constants
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

SIMILAR_ACCOUNT = "chefsteps"
USERNAME = EMAIL
BASE_URL = "https://app.100daysofpython.dev/services/share-a-naan"
LOGIN_URL = f"{BASE_URL}/login"

# Create the InstaFollower object and init driver
insta_follower = InstaFollower()

# Log into the site
insta_follower.login(username=USERNAME, password=PASSWORD, url=LOGIN_URL)

# Find all the followers for SIMILAR_ACCOUNT
insta_follower.find_followers(url=f'{BASE_URL}/u/{SIMILAR_ACCOUNT}', user=SIMILAR_ACCOUNT)

# Follow all followers in the list retrieved
insta_follower.follow()


