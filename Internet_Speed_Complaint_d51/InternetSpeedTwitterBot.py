'''
    InternetSpeedTwitterBot class which provides Selenium driver functionality and various methods.
'''
from selenium import webdriver
from selenium.webdriver.common.by import By, ByType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options

class InternetSpeedTwitterBot():
    def __init__(self, promised_download: float, promised_upload: float):
        # create a Chrome driver using provided chrome settings
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.down = promised_download
        self.up = promised_upload
    
    def login(self, email: str, password: str, url: str) -> None:
        ''' Automatically login to the Y test site to post a "tweet".'''
        # Start a selenium instance at the Y homepage
        self.driver.get(url)

        # Wait until the login_btn is visible
        wait = WebDriverWait(driver=self.driver, timeout=3)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "button")))

        # Notify user we're logging in (debug)
        print("--- Logging into Y account ---")

        # Sign in using Email and Password
        email_in = self.driver.find_element(By.ID, "email")
        password_in = self.driver.find_element(By.ID, "password")
        login_btn = self.driver.find_element(By.TAG_NAME, "button")

        email_in.clear()
        email_in.send_keys(email)
        password_in.clear()
        password_in.send_keys(password)
        login_btn.click()

        # wait for home page to load
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located((By.ID, "tweet-compose")))


    def get_internet_speed(self) -> dict[float, float]:
        ''' Automatically executes an internet speed test by going to a website to test internet speed.
            Returns a result dict containing the upload/download speeds.
        '''
        self.driver.get("https://www.speedtest.net/")
        
        # Wait for 90 seconds, as the speed test can take a bit
        wait = WebDriverWait(self.driver, 90)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class^='js-start-test']")))

        # Notify user we're running speed test (debug)
        print("--- Running internet speedtest ---")

        go_btn = self.driver.find_element(By.CSS_SELECTOR, "a[class^='js-start-test']")
        go_btn.click()

        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span[class$='upload-speed']"), text_="."))

        download_speed = float(self.driver.find_element(By.CSS_SELECTOR, "span[class$='download-speed']").text)
        upload_speed = float(self.driver.find_element(By.CSS_SELECTOR, "span[class$='upload-speed']").text)

        print(f'--- Speed Test Results ---')
        print(f'Download Speed: {download_speed} Mbps')
        print(f'Upload Speed: {upload_speed} Mbps')

        # Save results and in a dict and return to caller
        result = {
            'download': download_speed,
            'upload': upload_speed
        }

        return result


    def tweet_at_provider(self, test_upload: float, test_download: float) -> None:
        ''' Send a tweet (i.e., Y post) to the ISP. 
            NOTE: Requires user to be logged in already and at homepage!
        '''
        # Notify user we're running speed test (debug)
        print("--- Posting tweet about upload/download speeds ---")

        # Format and send tweet complaining about the promised speeds
        tweet = f"Hey Internet Provider, why is my internet speed {test_download} Mbps / {test_upload} Mbps when I pay for {self.down} Mbps / {self.up} Mbps?"
        print(tweet)
        tweet_field = self.driver.find_element(By.ID, "tweet-compose")
        tweet_field.clear()
        tweet_field.send_keys(tweet)

        # Click the "Post" button
        post_btn = self.driver.find_element(By.ID, "post-btn")
        post_btn.click()

