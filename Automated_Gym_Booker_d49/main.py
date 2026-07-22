'''
    This project is all about creating an automated gym booker using Selenium. It facilitates
    automatically filling in email, password, then logging in. Then it books Tue and Thu classes
    that are at 6:00 PM each, then automatically validates that they were booked by checking the
    "My Bookings" page.
'''

import os
import datetime as dt

from selenium import webdriver
from selenium.webdriver.common.by import By, ByType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# --- Constants ---
ACCOUNT_EMAIL = os.environ.get("ACCOUNT-EMAIL")
ACCOUNT_PASSWORD = os.environ.get("ACCOUNT-PASSWORD")
GYM_URL = "https://appbrewery.github.io/gym/"

# --- Globals ---
# Stats to record what bot processes such as booking, waitlist, or already booked
stats = {
    'booked': 0,
    'waitlist_joined': 0,
    'already_booked_or_waitlisted': 0,
}

# Used and set by Selenium calls
driver = None

# ----- Functions --------
def execute_automated_login() -> None:
    ''' Automatically fill in email, password, and click submit button to login to the site.'''
    global driver

    # Wait for page to load -- wait until Login button has loaded
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "login-button")))

    # Step 2: Automated login
    login_btn = driver.find_element(By.ID, "login-button")
    login_btn.click()

    # Wait for page to load -- wait until Submit button has loaded
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "submit-button")))

    # Fill in textboxes and click "Login" button
    email = driver.find_element(By.NAME, "email")
    password = driver.find_element(By.NAME, "password")
    submit_btn = driver.find_element(By.ID, "submit-button")

    email.clear()
    email.send_keys(ACCOUNT_EMAIL)
    password.clear()
    password.send_keys(ACCOUNT_PASSWORD)

    submit_btn.click()

def retry_wrapper(func, error_msg: str, by_type: ByType, retries: int=3) -> None:
    ''' Retry wrapper to attempt the func for retries amount. Look for error_msg on page and wait for wait_element.'''
    global driver
    attempt_num = 0

    while attempt_num <= retries:
        func()

        # Wait for page to load -- wait until error is shown button has loaded
        try:
            wait = WebDriverWait(driver, 3)
            wait.until(EC.presence_of_element_located((by_type, error_msg)))
        # If it times out, then that means we got to the next page, so break out of loop
        except TimeoutException:
            break
        else:
            # Check if error message is on the screen
            error = driver.find_element(by_type, error_msg)

            if error:
                attempt_num += 1
                print(f'Network issue! Retrying...attempt {attempt_num}...')
            else:
                break
    
    if attempt_num == retries:
        print(f"Max retries = {retries} met")

def fmt_date(day: str) -> dict:
    ''' Format the day of week, month, and day of month and return.'''
    # Expected example inputs:
        # Today (Thu, Jun 11)
        # Tomorrow (Thu, Jun 11)
        # Thu, Jun 11

    today = {}

    if 'Today' in day or 'Tomorrow' in day:
        day = day.split('(')[1][:-1]
    
    today = {
        'dayOfWeek': day.split(',')[0],
        'month': day.split(',')[1].strip().split()[0],
        'dayOfMonth': day.split(',')[1].strip().split()[1]
    }
    return today

def get_classes_for_day(classes: list[WebElement], dayOfWeek: str) -> tuple[WebElement,str]:
    '''Get the list of classes for the dayOfWeek and date for the day as a tuple.'''
    # Look at each day in the total list of classes
    day_classes = None
    day_date = None

    for day in classes:
        curr_day = day.find_element(By.CSS_SELECTOR, "h2[id^='day-title']").text
        # Check if it's the dayOfWeek we want
        if dayOfWeek in curr_day:
            day_classes = day
            day_date = fmt_date(curr_day)
    
    return [day_classes, day_date]

def book_classes(day_classes: WebElement, day_date: dict, book_time: str, book_stats: dict) -> None:
    '''Book the class on the specified day_date at the book_time. Return the stats of what was booked.'''
    # Iterate through each card class
    cards = day_classes.find_elements(By.CSS_SELECTOR, "div[id^='class-card']")

    for card in cards:
        class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name']")
        class_time = card.find_element(By.CSS_SELECTOR, "p[id^='class-time']")

        if book_time in class_time.text:
            button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button']")

            # wait = WebDriverWait(driver, 10)
            # button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id^='book-button']")))

            if button.text == 'Booked':
                print(f'✅ Already Booked: {class_name.text} on {day_date['dayOfWeek']}, {day_date['month']} {day_date['dayOfMonth']}')
                book_stats['already_booked_or_waitlisted'] += 1
            elif button.text == 'Waitlisted':
                print(f'✅ Already on waitlist: {class_name.text} on {day_date['dayOfWeek']}, {day_date['month']} {day_date['dayOfMonth']}')
                book_stats['already_booked_or_waitlisted'] += 1
            elif button.text == 'Join Waitlist':
                # button.click()
                # Click it using JavaScript to bypass the interception
                # driver.execute_script("arguments[0].click();", button)
                # Check for button actually clicked
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", button)
                retry_wrapper(func=button.click, error_msg="div[id^='class-error']", by_type=By.CSS_SELECTOR, retries=3)
                print(f'✅ Joined waitlist for: {class_name.text} on {day_date['dayOfWeek']}, {day_date['month']} {day_date['dayOfMonth']}')
                book_stats['waitlist_joined'] += 1
            else:
                # button.click()
                # Click it using JavaScript to bypass the interception
                # driver.execute_script("arguments[0].click();", button)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", button)
                retry_wrapper(func=button.click, error_msg="div[id^='class-error']", by_type=By.CSS_SELECTOR, retries=3)
                print(f'✅ Booked: {class_name.text} on {day_date['dayOfWeek']}, {day_date['month']} {day_date['dayOfMonth']}')
                book_stats['booked'] += 1
            break
    
    return None

def print_book_stats(book_stats: dict, dayOfWeek: str, book_time: str) -> None:
    ''' Print the booking stats for the specified dayOfWeek and book_time '''
    print("\n--- BOOKING SUMMARY ---")
    print(f'Classes booked: {book_stats['booked']}')
    print(f'Waitlists joined: {book_stats['waitlist_joined']}')
    print(f'Already booked/waitlisted: {book_stats['already_booked_or_waitlisted']}')
    print(f'Total {dayOfWeek} {book_time} classes processed: {sum(book_stats.values())}')

def print_verification(is_booked: bool, day: str, book_time: str, class_name: str) -> None:
    ''' Prints whether the bookings made were verified for the specified is_booked on the day.'''
    if is_booked:
        print(f'✅Verified {day} booking for {class_name} at {book_time}')
    else:
        print(f'❌Error: Did not book {day} {f'for {class_name}' if class_name else "class"} at {book_time}!')

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Create a Chrome profile to restore database and settings when running script
user_data_dir = os.path.join(os.getcwd(), "chrome-profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# create a Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Start a selenium instance at the gym homepage
driver.get(GYM_URL)

# Step 1: Automatically login
print('--- Logging in --- ')
retry_wrapper(func=execute_automated_login, by_type=By.ID, error_msg="error-message", retries=3)

# Wait for page to load -- wait until Logout button has loaded
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, "logout-button")))

# --- Book the upcoming Tue and Thu class ---

# Get the list of classes for all days
classes = driver.find_elements(By.CSS_SELECTOR, "div[id^='day-group']")

# Get Tue and Thu classes and their dates formatted
tuesday_classes, tuesday_date = get_classes_for_day(classes=classes, dayOfWeek='Tue')
tuesday_book_stats = dict(stats)
thursday_classes, thursday_date = get_classes_for_day(classes=classes, dayOfWeek='Thu')
thursday_book_stats = dict(stats)
book_time = "6:00 PM"

# Book Tue and Thu classes at '6:00 PM'
print('--- Booking classes --- ')
book_classes(day_classes=tuesday_classes, day_date=tuesday_date, book_time=book_time, book_stats=tuesday_book_stats)
book_classes(day_classes=thursday_classes, day_date=thursday_date, book_time=book_time, book_stats=thursday_book_stats)

# --- Verify Class bookings on the "My Bookings" page ---
is_tue_verified = False
is_thu_verified = False
bookings_link = driver.find_element(By.ID, 'my-bookings-link')
bookings_link.click()

print('\n--- VERIFYING ON MY BOOKINGS PAGE --- ')

# Wait for page to load -- wait until Login button has loaded
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[class^='MyBookings_page']")))

# Select the Confirmed booking cards
try:
    bookings = driver.find_elements(By.CSS_SELECTOR, "div[id^='booking-card']")
    if len(bookings) == 0:
        raise NoSuchElementException
except NoSuchElementException:
    print('❌Error: No bookings found on the My Bookings page!')
else:
    tue_class_name = ""
    thu_class_name = ""

    # Check confirmed bookings
    for booking in bookings:
        verified_book_time = booking.find_element(By.CSS_SELECTOR, 'p').text
        class_name = booking.find_element(By.TAG_NAME, "h3").text

        if 'Tue' in verified_book_time and book_time in verified_book_time:
            is_tue_verified = True
            tue_class_name = class_name
        elif 'Thu' in verified_book_time and book_time in verified_book_time:
            is_thu_verified = True
            thu_class_name = class_name
    
    # Check Waitlist (if any)
    waitlists = driver.find_elements(By.CSS_SELECTOR, "div[id^='waitlist-card']")

    if waitlists:
        for waitlist in waitlists:
            verified_book_time = waitlist.find_element(By.CSS_SELECTOR, 'p').text
            class_name = waitlist.find_element(By.TAG_NAME, "h3").text

            if 'Tue' in verified_book_time and book_time in verified_book_time:
                is_tue_verified = True
                tue_class_name = class_name
            elif 'Thu' in verified_book_time and book_time in verified_book_time:
                is_thu_verified = True
                thu_class_name = class_name

    print_verification(is_booked=is_tue_verified, day='Tuesday', book_time=book_time, class_name=tue_class_name)
    print_verification(is_booked=is_thu_verified, day='Thursday', book_time=book_time, class_name=thu_class_name)

# Print out statistics for each day
print_book_stats(book_stats=tuesday_book_stats, dayOfWeek=tuesday_date['dayOfWeek'], book_time=book_time)
print_book_stats(book_stats=thursday_book_stats, dayOfWeek=thursday_date['dayOfWeek'], book_time=book_time)

# driver.quit()