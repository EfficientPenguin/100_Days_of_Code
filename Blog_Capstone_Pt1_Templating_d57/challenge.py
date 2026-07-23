
'''
    Challenge from Day 56: At /guess/{name}, return a dynamic web page
    using Flask that leverages/uses Jinja templating to achieve the desired result.
    Use the genderize API and agify API which are free and require no authentication.
    Agify will return a dict with the age we need to extract based on the name; 
    Genderize will return the guessed gender based on the name.

    The second part makes me practice multiline statements in Jinja by reading blog posts
    from a specific API provided by Angela Yu @appbrewery.
'''

import random
import datetime as dt

from flask import Flask, render_template
import requests

# API endpoints for genderize and agify
GENDERIZE_ENDPOINT = "https://api.genderize.io"
AGIFY_ENDPOINT = "https://api.agify.io"
BLOG_ENDPOINT = "https://api.npoint.io/c790b4d5cab58020d391"

# Functions to get HTTP
def get_gender(name: str) -> str:
    ''' Get the gender from the Genderize API and return as a str using the name param.'''
    params = {
        'name': name
    }
    response = requests.get(GENDERIZE_ENDPOINT, params=params)
    response.raise_for_status()

    return response.json()["gender"]

def get_age(name: str) -> int:
    ''' Get the gender from the Genderize API and return as a str using the name param.'''
    params = {
        'name': name
    }
    response = requests.get(AGIFY_ENDPOINT, params=params)
    response.raise_for_status()

    return int(response.json()["age"])

app = Flask(__name__)

@app.route('/')
def home_route():
    return render_template('index.html')

@app.route('/guess/<name>')
def guess_route(name):
    gender = get_gender(name)
    age = get_age(name)
    return render_template("challenge.html", name=name, gender=gender, age=age)

@app.route('/blog')
def get_blog():
    # Get the blogs and print out the list
    response = requests.get(BLOG_ENDPOINT)
    # print(response.json())
    posts = response.json()


    return render_template("blog.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)