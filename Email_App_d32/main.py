'''
    This app implements a simple email sender for birthdays.
'''

import datetime as dt
import random
import os

import smtplib
import pandas

email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

# Get my birthday for this year
today = dt.datetime(year=2026,month=5,day=31)

# Read in from the birthdays.csv
df = pandas.read_csv(filepath_or_buffer="birthdays.csv")
# print(df[(df[df['month'] == 5]) & (df[df['day'] == 31])])
row = df[df.day == 31]
print(row.name)

# Select a random file from a set of 3 files
letters = ["letter1.txt", "letter2.txt", "letter3.txt"]
letter = random.choice(letters)

# Replace the [NAME] with the person's birthday that's today
with open(file=letter, mode="r") as file:
    content = file.readlines()

for i in range(len(content)):
    content[i] = content[i].replace('[NAME]', str(row.name.item()))

content = "".join(content)

# Send an email to myself as the birthday person
with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=email, password=password)
    connection.sendmail(
        from_addr=email,
        to_addrs=email,
        msg=f"Subject:Birthday Email!\n\n{content}."
    )