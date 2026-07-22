'''
    This Selenium bot automatically signs into a TinderBot page, and starts swipping right (i.e., clicking the like button) 
    to match with made-up dogs.

    NOTE: Make sure you run "rm -rf chrome-profile" (if it exists) BEFORE running the script for things to work correctly.
          See the .env file for email and password used for this script. Naviaget to the appbrewery login page
          to configure my connection to the test site. 
'''

import os
import datetime as dt
from time import time, sleep

from selenium import webdriver
from selenium.webdriver.common.by import By, ByType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

from dotenv import load_dotenv

# Load in .env variables
load_dotenv()

# CONSTANTS
TINDER_BOT_URL = "https://app.100daysofpython.dev/services/tindog/u/uixAMX5OpHnWfA3bTWM3RGJrKeiT4IK1"
FACEBARK_EMAIL = os.environ.get("FACEBARK_EMAIL")
FACEBARK_PASSWORD = os.environ.get("FACEBARK_PASSWORD")

# Tinder bot daily swipe limit
DAILY_SWIPE_LIMIT = 20

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Create a Chrome profile to restore database and settings when running script
user_data_dir = os.path.join(os.getcwd(), "chrome-profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# create a Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Start a selenium instance at the gym homepage
driver.get(TINDER_BOT_URL)

# Wait for the "Login" button to show
wait = WebDriverWait(driver, 2)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='button']")))

# Click on login button
login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='button']")
login_btn.click()

sleep(2)
facebark_btn = driver.find_element(By.CLASS_NAME, "btn-facebark")
facebark_btn.click()

# Login opens a new window, so get all handles, then handle new pop-up window
driver.window_handles
base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]

# Switch to Facebark login window
driver.switch_to.window(fb_login_window)
sleep(1)

# Auto-populate fields
email = driver.find_element(By.NAME, "email")
email.clear()
email.send_keys(FACEBARK_EMAIL)
password = driver.find_element(By.NAME, "pass")
password.clear()
password.send_keys(FACEBARK_PASSWORD)
submit_btn = driver.find_element(By.TAG_NAME, "button")
submit_btn.click()

# Swap back to main window, as login will close
driver.switch_to.window(base_window)

# Click Ok for subsequent screens until you get to home page where we start swipping
# Wait for the "popup for location" button to show
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class^='popup-overlay']")))

# Click on "Allow" button for location
allow_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
allow_btn.click()

# Wait for the "popup for location" button to show
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class^='popup-overlay']")))

# Click on "Enable" button for location
enable_btn = driver.find_element(By.CSS_SELECTOR, "button[class='btn-primary']")
enable_btn.click()

# Wait for the "popup for cookies" button to show
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class^='popup-overlay']")))

# Click on "I accept" button for location
i_accept_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
i_accept_btn.click()

# --- Start Swipping ---
# Limited to 20 swipes per day on TinDog!
dogs_liked = 0
while dogs_liked < DAILY_SWIPE_LIMIT:
    sleep(1)
    # Swipe once, then check if pop-up shows
    try:
        like_btn = driver.find_element(By.CSS_SELECTOR, "button[class='btn-like']")
        # Scroll to the button and click it. Bug: Have to scroll several times for it
        # to actually scroll to the button 
        for _ in range(35):
            driver.execute_script("arguments[0].scrollIntoView(true);", like_btn)

        like_btn.click()
    except ElementClickInterceptedException:
        try:
            driver.find_element(By.CSS_SELECTOR, value='.match-popup a').click()
        except NoSuchElementException:
            sleep(2)
    except NoSuchElementException:
        # Like button not loaded yet OR all dogs have been swiped -- wait and retry
        sleep(2)
    else:
        # Like button successfully clicked, so update counter
        dogs_liked += 1

# driver.quit