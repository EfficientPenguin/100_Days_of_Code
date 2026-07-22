'''
    This application is all about practicing Selenium where I scrape from a webssite, automate
    filling out data/forms on a website, cookie clicker project, and create an automated game playing
    bot.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# create a Chrome driver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.amazon.com/ASUS-Graphics-3-8-Slot-Axial-tech-Phase-Change/dp/B0DS2WQZ2M?crid=384RRPR28WXYP&dib=eyJ2IjoiMSJ9.HnfcaEKxhyXDrTSjKHg7HhkJWDxda7I47hxNgk7zFUBFWbevbgcGghArkgZaLg8YNRKABa2jXOkWk90lAqwki8sucXSOhrlxMPdSv166den96e018XMGxn02NqqPl_qO-ZIQJBYIZaDzBypeipZeOEdjmb0ujKwBQQ4LiMzBX2Z9lJPHEaXEg18sskw1nd_gdjgMdck5pK0GgqDPrZIO0oTpE7uL7sCMJGG5QKatD_0.SZnWNXjbD-Fyj8Sgt_WePtpgQuqrXT5sDeUHjC5d_Ig&dib_tag=se&keywords=5090%2Bgraphics%2Bcard&qid=1781030349&sprefix=5090%2B%2Caps%2C113&sr=8-1&th=1")

# Get the price data from the page using selenium
price_dollar = driver.find_element(By.CLASS_NAME, value="a-price-whole")
price_cents = driver.find_element(By.CLASS_NAME, "a-price-fraction")

print(f"The price is {price_dollar.text}.{price_cents.text}")

search_bar_name = driver.find_element(By.NAME, value="field-keywords").get_attribute(name="placeholder")
print(search_bar_name)

# driver.close()
driver.quit()

