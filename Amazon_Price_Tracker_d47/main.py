'''
    This application will scrape an Amazon site for a product's price, check whether it hits or falls below some
    threshold price, then sends me an email if it meets the price condition. Good practice for bs4 and smtplib
'''

import smtplib
import json
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SMTP_ADDRESS = os.environ.get("SMTP_ADDRESS")

GPU_WEBSITE = "https://www.amazon.com/ASUS-Graphics-3-8-Slot-Axial-tech-Phase-Change/dp/B0DS2WQZ2M?crid=384RRPR28WXYP&dib=eyJ2IjoiMSJ9.HnfcaEKxhyXDrTSjKHg7HhkJWDxda7I47hxNgk7zFUBFWbevbgcGghArkgZaLg8YNRKABa2jXOkWk90lAqwki8sucXSOhrlxMPdSv166den96e018XMGxn02NqqPl_qO-ZIQJBYIZaDzBypeipZeOEdjmb0ujKwBQQ4LiMzBX2Z9lJPHEaXEg18sskw1nd_gdjgMdck5pK0GgqDPrZIO0oTpE7uL7sCMJGG5QKatD_0.SZnWNXjbD-Fyj8Sgt_WePtpgQuqrXT5sDeUHjC5d_Ig&dib_tag=se&keywords=5090%2Bgraphics%2Bcard&qid=1781030349&sprefix=5090%2B%2Caps%2C113&sr=8-1&th=1"
HTML_FILE = "amazon_gpu_page.html"

PRICE_THRESHOLD = 4499.99

# Get theh website using requests
response = requests.get(url=GPU_WEBSITE)
response.raise_for_status()

# with open(file=HTML_FILE, mode="w") as file:
#     file.write(response.text)

# Check the response code for good status
print(response.status_code)

# Extract the price and print it to verify it's correct
soup = BeautifulSoup(response.text, 'html.parser')

whole = soup.find("span", class_="a-price-whole").getText()
decimal = soup.find("span", class_="a-price-fraction").getText()

price = float(f"{"".join(whole.split(","))}{decimal}")

# Compare to threshold
if price <= PRICE_THRESHOLD:
    print(f"{price} is less than {PRICE_THRESHOLD}! Sending email...")

    # If it meets threshold, then send email to myself
    content = f"GeForce RTX 5090 32GB GDDR7 OC Edition Gaming Graphics Card price is ${price} which is below \
        price threshold of ${PRICE_THRESHOLD}.\n\nLink to product: {GPU_WEBSITE}"

    # Send an email to myself as the birthday person
    with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_ADDRESS,
            to_addrs=EMAIL_ADDRESS,
            msg=f"Subject:GPU Price Alert!\n\n{content}."
    )