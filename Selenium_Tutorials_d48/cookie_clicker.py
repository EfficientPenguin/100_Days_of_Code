'''
    This project implements a Python/Selenium bot to play the cookie clicker game for 5mins before terminating.
    The goal is to use what I've learned about Selenium using day 48's lessons to have it automatically play the game.
    Optionally I can play the game alongside the bot in another browser, then compare the results for some added fun!
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Time Constants in seconds
SEC_PER_MIN = 60
PLAY_TIME =  SEC_PER_MIN * 5
COOKIE_CLICK_TIME = 5

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# create a Chrome driver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://ozh.github.io/cookieclicker/")

# Select the language as English
time.sleep(3)
eng_lang_btn = driver.find_element(By.ID, "langSelect-EN")
eng_lang_btn.click()

time.sleep(3)
# Setup cookie clicker obj
cookie = driver.find_element(By.ID, "bigCookie")
cookie_score = driver.find_element(By.ID, "cookies")

# Set a timer for 300 seconds (i.e., 5min), clicking the cookie as fast as possible
start_time = time.time()

while(time.time() - start_time < PLAY_TIME):
    print(f'clicking cookie for {COOKIE_CLICK_TIME} sec')
    cookie_time = time.time()
    while time.time() - cookie_time < COOKIE_CLICK_TIME:
        cookie.click()
    print('checking products to buy...')

    # Check for upgrades and buy most expensive one that I can afford
    curr_score = (cookie_score.text).split(' ')[0]
    if ',' in curr_score:
        curr_score = "".join(curr_score.split(','))
    curr_score = int(curr_score)

    buy_upgrade = None

    products = driver.find_elements(By.ID, "products")
    unlocked_products = driver.find_elements(By.CLASS_NAME, "unlocked") 

    # Find the max we can afford and buy
    for i, product in enumerate(unlocked_products):
        price = product.find_element(By.CLASS_NAME, "price").text
        if ',' in price:
            price = "".join(price.split(','))
        price = int(price)

        if curr_score >= price:
            buy_upgrade = product
    
    # Buy the upgrade
    if buy_upgrade is not None:
        buy_upgrade.click()
        print(f'Buying {buy_upgrade.text}')


# Print cookie rate; keep polling until I can read it, as upgrades may "auto-click" and update class_name containing the rate
cookie_score = driver.find_element(By.ID, "cookies")
cookie_rate = driver.find_element(By.ID, "cookiesPerSecond")

print(cookie_score, cookie_rate)
while (cookie_rate is None or cookie_score is None):
    cookie_rate = driver.find_element(By.ID, "cookiesPerSecond")
    cookie_score = driver.find_element(By.ID, "cookies")
print(f'Cookie Click rate: {cookie_rate.text.split(' ')[2]} cookies per second')
print(f'Total cookie score: {cookie_score.text}')
        
        

driver.quit()





