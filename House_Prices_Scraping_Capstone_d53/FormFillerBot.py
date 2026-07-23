'''
    Class to fill in Google Sheets form automatically using the property data we extracted.
'''
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FormFillerBot():
    def __init__(self):
        # Init the driver
        # Set the chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        # Create the driver
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def fill_form(self, url: str, address: str, price: int, link: str) -> None:
        ''' Fill the data on the form: Address, Price, and URL of the property.'''
        self.driver.get(url=url)

        # Wait for form to load
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
                   
        # Target all text boxes, and the 'Submit' button
        text_boxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "div[role='button']")

        address_box = text_boxes[0]
        price_box = text_boxes[1]
        link_box = text_boxes[2]

        address_box.clear()
        address_box.send_keys(address)

        price_box.clear()
        price_box.send_keys(price)

        link_box.clear()
        link_box.send_keys(link)

        submit_btn.click()
        sleep(1)
        


