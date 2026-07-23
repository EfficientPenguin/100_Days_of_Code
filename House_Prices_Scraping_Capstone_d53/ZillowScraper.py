'''
    This class extracts the Zillow data from the Zillow site.
'''
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet

from PropertyData import PropertyData

class ZillowScraper():
    def __init__(self, url: str):
        self.url = url
        self.property_listings = None

    def get_property_listings(self) -> None:
        ''' Get the property listings from the site and store in member variable.'''
        # Get the Zillow clone info using requests library
        response = requests.get(url=self.url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Store the property listings for later
        self.property_listings = soup.select("ul > li[class$='StyledListCardWrapper']")
    
    def get_property_data(self) -> list[PropertyData]:
        ''' Extract the property prices, address, and url from the property_listings.'''
        property_data_list = []

        # Get the price for each property
        if self.property_listings:
            # Search through the listings
            for listing in self.property_listings:
                # Get the Price, Address, and URL for the property
                price = listing.select_one("span[class$='StyledPriceLine']").text
                address = listing.select_one("address[data-test='property-card-addr']").text
                url = listing.select_one("a[class='property-card-link']").get("href")

                # print(f'Original: {price} | Formatted: {fmt_price}')
                property_data_list.append(PropertyData(price, address, url))
        return property_data_list

