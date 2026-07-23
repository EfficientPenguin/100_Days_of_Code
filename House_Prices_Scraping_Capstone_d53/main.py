'''
    This application is a capstone for Day 53: Web Scraping and Data Entry project. The goal is to scrape several
    items from a Zillow website clone developed by appbrewery, then fill out a form with the details pertaining to
    the search. It brings all the skills together for bs4 and Selenium.

    Plan: Use BeautifulSoup to extract Price, Address, and URL info from the Zillow site. Use Selenium to auto-fill a 
    Google Form. Option: At the end, manually click "Link to Sheets" to automatically create a spreadsheet with all of
    the collected data.
'''

import requests
from bs4 import BeautifulSoup

from ZillowScraper import ZillowScraper
from FormFillerBot import FormFillerBot

# Constants
ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeAl1nWttDxtbD3kNIvy--4_UtaHNKdIyZOUplpxHEwbkRgTA/viewform?usp=publish-editor"

# 1. Setup Google Form
# 2. Play around with fake Zillow site to see how it's constructed
# 3. Use bs4 to scrape all listings from the Zillow-clone website
# 4. Use selenium to fill in the form you created in 1

# Create scraper and form filler bot
zillow_scraper = ZillowScraper(ZILLOW_CLONE_URL)
form_filler_bot = FormFillerBot()

# Get the property listings
zillow_scraper.get_property_listings()

# Get the property data
property_data = zillow_scraper.get_property_data()

# Print it out
# for property in property_data:
#     print(' ----------------')
#     print(property.price)
#     print(property.address)
#     print(property.url)

# Fill in a form for each property in the list
for property in property_data:
    form_filler_bot.fill_form(url=FORM_URL, 
                              address=property.address, 
                              price=property.price, 
                              link=property.url)