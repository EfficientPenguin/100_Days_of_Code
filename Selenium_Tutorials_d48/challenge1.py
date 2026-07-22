'''
    This challenge is to pull the upcoming dates from the pyplace and load them in as a dictinoary.
    Use selenium to pull ALL of the upcoming events into Python, then create the dict, then print it out.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# create a Chrome driver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.python.org/")

# Get the Event dates and names
event_dates = driver.find_elements(By.CSS_SELECTOR, value=".event-widget time")
event_names = driver.find_elements(By.CSS_SELECTOR, value=".event-widget li a")

for event_date, event_name in zip(event_dates, event_names):
    print(f'{event_date.text}\t{event_name.text}')

# Create the nested dict
events = {i:{'time':event_dates[i].text, 'name':event_names[i].text} for i in range(len(event_dates))}

print(events)


driver.quit()
