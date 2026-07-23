'''
    This application automatically tests the current upload/download speed of my ISP, then it posts on X (or the appbrewery equivalent)
    complaining about the current internet speeds I'm getting.
'''

import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By, ByType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

from InternetSpeedTwitterBot import InternetSpeedTwitterBot

# Load .env variables
load_dotenv()

# --- Constants ---
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
Y_URL = "https://app.100daysofpython.dev/services/y/login"
PROMISED_DOWN = 1000
PROMISED_UP = 1000

# # Keep Chrome browser open after program finishes
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)

# # Create a Chrome profile to restore database and settings when running script
# user_data_dir = os.path.join(os.getcwd(), "chrome-profile")
# chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# create a InternetSpeedTwitterBot object and init with chrome_options
isp_twit_bot = InternetSpeedTwitterBot(promised_download=PROMISED_DOWN, promised_upload=PROMISED_UP)

# Execute speed test using Isp twit bot
test_results = isp_twit_bot.get_internet_speed()

# Login to the Y page
isp_twit_bot.login(email=EMAIL, password=PASSWORD, url=Y_URL)

# Post a tweet complaining about promised upload/download speeds
isp_twit_bot.tweet_at_provider(test_upload=test_results['upload'], test_download=test_results['download'])

