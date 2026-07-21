'''
    This application pulls data from the ISS API and sends an email after parsing the data. The second half
    of the day focuses on building a Kanye Rest API (lol)
'''

import requests

def get_iss_position() -> None:
    ''' Fetches ISS current location using requests library and prints it to console. '''
    response = requests.get(url="http://api.open-notify.org/iss-now.json")

    # Check for any error status. Requests provides a built-in way to raise exceptions so we don't have long if-elif-elif...else
    response.raise_for_status()

    data = response.json()

    longitude = data['iss_position']['longitude']
    latitude = data['iss_position']['latitude']

    iss_position = (longitude, latitude)
    print(iss_position)


# Kanye Rest API
def kanye_west_quote_generator() -> None:
    ''' Fetch API data from Kanye west URL and print out the random quote.'''

    # Pull data from here: https://kanye.rest/
    response = requests.get(url="https://api.kanye.rest/")
    response.raise_for_status()

    # Get it in JSON format
    data = response.json()

    # Print the quote
    print(data['quote'])

def get_sunset_times() -> None:
    ''' More URL practice. Get the sunset times for my particular location in lat and long and display it.'''

    parameters = {
        "lat": 39.099529,
        "lng": -76.848373,
        "tzid": "America/New_York"
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    # Get it in JSON format
    data = response.json()

    sunset = data['results']['sunset']
    sunrise = data['results']['sunrise']

    # Print out the data
    print(f"Sunrise:\t{sunrise}\nSunset:\t\t{sunset}")

get_sunset_times()