'''
    This challenge is to practice pulling data from the Wikipedia homepage using Selenium.
    The app simply extracts the article count in the header and displays the total number of articles
    in Wikipedia. This part was commented out -- now the code fills in textboxes and clicks a signup button
    on the appbrewery sample page.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# create a Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# driver.get("https://en.wikipedia.org/wiki/Main_Page")

# # Extract the data using the driver.find_element(By.t)
# num_articles = driver.find_elements(By.CSS_SELECTOR, "#articlecount li a")[1]

# print(num_articles.text)

# # Click on the wikibooks link on the Wiki homepage
# # driver.find_element(By.LINK_TEXT, value="Wikibooks").click()

# # Search for the textbox to search for "Python", then hit ENTER to go to the results page
# search = driver.find_element(By.NAME, value="search")
# search.send_keys("Python", Keys.ENTER)

# driver.quit()

# CHALLENGE: Fill in appbrewery page with info then click sign up
driver.get("https://appbrewery.github.io/fake-newsletter-signup/")

# Fill in each textbox
textbox = driver.find_element(By.CLASS_NAME, value="top")

# Fill in the data for the textbox
textbox.send_keys("FirstName")

# Repeat for other textboxes
textbox = driver.find_element(By.CLASS_NAME, value="middle")
textbox.send_keys("LastName")

textbox = driver.find_element(By.CLASS_NAME, value="bottom")
textbox.send_keys("FirstName.LastName@gmail.com")

# Click the button
signup_button = driver.find_element(By.CLASS_NAME, value="btn")
signup_button.click()


