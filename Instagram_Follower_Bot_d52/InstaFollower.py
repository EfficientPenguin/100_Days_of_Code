'''
    This class implements functionality that deals with logging in and following people on the
    fake Instagram test website "Share-a-Naan".
'''

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstaFollower():
    def __init__(self):
        # Set the chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        # Create the driver
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self, username: str, password: str, url: str) -> None:
        ''' Automatically logs into the Share-A-Naan website using username and password.'''
        # Go to the webpage
        self.driver.get(url)

        # Wait until username text is shown
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located((By.ID, "username")))

        # Login using USERNAME and PASSWORD
        username_in = self.driver.find_element(By.ID, "username")
        password_in = self.driver.find_element(By.ID, "password")
        login_btn = self.driver.find_element(By.TAG_NAME, "button")

        username_in.clear()
        username_in.send_keys(username)
        password_in.clear()
        password_in.send_keys(password)

        login_btn.click()

        # Wait until pop up for save login is shown
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='naan-popup-dismiss']")))

        save_login_popup_dismiss = self.driver.find_element(By.CSS_SELECTOR, "div[class='naan-popup-dismiss']")
        save_login_popup_dismiss.click()

        # Wait until pop up for save login is shown
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[class='naan-popup-dismiss']")))

        notifications_popup_dismiss = self.driver.find_element(By.CSS_SELECTOR, "button[class='naan-popup-dismiss']")
        notifications_popup_dismiss.click()

        # Wait until pop up for save login is shown
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/services/share-a-naan']")))

    def find_followers(self, url: str, user: str) -> None:
        ''' Find the followers for a given user. 
            NOTE: Assumes already logged in!
        '''
        self.driver.get(url)

        # Wait until profile name is visible
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='naan-profile-name']")))

        followers_link = self.driver.find_element(By.CSS_SELECTOR, "a[class='naan-followers-link']")
        followers_link.click()

        # Wait until followers list popup is visible
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Followers']")))


    def follow(self) -> None:
        ''' Follow a user.
            NOTE: Assumes you're looking at the Followers popup.'''
        # Get list of followers
        followers = self.driver.find_elements(By.CSS_SELECTOR, "div[class='naan-follower-row']")

        # Followers is a list, so we need to look at each follower to follow
        for follower in followers:
            name_handle = follower.find_element(By.CSS_SELECTOR, "div[class='naan-handle']").text

            # Scroll to the row being inspected
            self.driver.execute_script("arguments[0].scrollIntoView(true);", follower)

            # Target the follow button for the current row
            follow_btn = follower.find_element(By.TAG_NAME, "button")

            # Click the button to follow; else, we're already following
            if follow_btn.text == "Follow":
                follow_btn.click()
            
            # 1 sec delay to seem more human and not bot-like
            sleep(1)
        
        # Close the popup window after following all in the followers list
        close_btn = self.driver.find_element(By.CSS_SELECTOR, "a[class='naan-modal-close']")
        close_btn.click()
