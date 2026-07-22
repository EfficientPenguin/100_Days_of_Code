'''
    This application implements a simple stock trading news alert system. It uses the alphavantage.co
    API. First it fetches the technical data from alphavantage, calculates the difference between
    closing price of last trading day and the day before that, calculates the percent change, and if it
    exceeds a 2% threshold, then it will trigger a news article request. The top 5 are formatted and sent
    as an email to myself -- pretty cool!
'''

import json
import datetime
import smtplib
import os

import requests
import requests_cache

# Alphavantage api key
api_key = os.environ.get("API-KEY")

# Send email to myself of the top 5 articles of TSLA
email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

# ----------- Technical Data Request -----------
url = "https://www.alphavantage.co/query"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "interval": "5min",
    "apikey": api_key
}

# Patch all requests globally
requests_cache.install_cache('global_cache', expire_after=-1)

# Get the stock price data for the past two days
response = requests.get(url=url, params=params)
response.raise_for_status()

data = response.json()

# Write it to a file for assistance with parsing json, etc.
with open(file='tsla.json', mode='w') as file:
    json.dump(data, file, indent=4)

# Iterate over Time Series (Daily) to pull the closing price data
yesterday_close = None
before_yesterday = None
day_cnt = 0

def fmt_date(date):
    return date.strftime("%Y-%m-%d")

# Read in the pertinent data for the last two trading days
today = datetime.datetime.today()
prev = today - datetime.timedelta(days=1)

while fmt_date(prev) not in data["Time Series (Daily)"].keys():
    prev = prev - datetime.timedelta(days=1)

last_trading_day = (fmt_date(prev), float(data["Time Series (Daily)"][fmt_date(prev)]["4. close"]))
prev = prev - datetime.timedelta(days=1)

while fmt_date(prev) not in data["Time Series (Daily)"].keys():
    prev = prev - datetime.timedelta(days=1)

second_to_last_trading_day = (fmt_date(prev), float(data["Time Series (Daily)"][fmt_date(prev)]["4. close"]))

print(response.from_cache)
print(last_trading_day, second_to_last_trading_day)

# Calculate the price differential.
closing_price_difference = last_trading_day[1]-second_to_last_trading_day[1]
percent_gain_loss = closing_price_difference/last_trading_day[1]*100
print(f'Closing price difference: {percent_gain_loss:.02f}%')

# Trigger alert and fetch news data using api too?
if abs(percent_gain_loss) > 2.0:
    print('TSLA is trending down!')

    time_from = second_to_last_trading_day[0].split('-')
    time_to = last_trading_day[0].split('-')

    # ----------- News Request -----------
    news_url = "https://www.alphavantage.co/query"

    news_params = {
        "function": "NEWS_SENTIMENT",
        "tickers": "TSLA",
        "time_from": f'{time_from[0]}{time_from[1]}{time_from[2]}T0000',
        "time_to": f'{time_to[0]}{time_to[1]}{time_to[2]}T2359',
        "apikey": api_key
}

    # Get the stock price data for the past two days
    news_response = requests.get(url=news_url, params=news_params)
    news_response.raise_for_status()

    data = news_response.json()

    # Write it to a file for assistance with parsing json, etc.
    with open(file='tsla_news.json', mode='w') as file:
        json.dump(data, file, indent=4)

    # Only report title and summary of top 5 latest articles
    article_num = 0
    articles_fmtd = []

    while(article_num < 5):
        article = {}
        article['title'] = data['feed'][article_num]['title']
        article['summary'] = data['feed'][article_num]['summary']
        articles_fmtd.append(article)
        article_num += 1

    print(articles_fmtd)
    print(news_response.from_cache)

    content = ''
    cnt = 1
    for article in articles_fmtd:
        content += f'{cnt}: {article['title']}\nBrief: {article['summary']}\n\n'

    # Send an email to myself with the top 5 latest articles from TSLA for the past two trading days as range
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(
            from_addr=email,
            to_addrs=email,
            msg=f"Subject:TSLA Trending!\n\n{content}."
        )
    