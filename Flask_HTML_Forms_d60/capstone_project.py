
'''
    Add HTML Form Entry capability to Capstone Project from Day 59.
'''

import os

from flask import Flask, render_template, url_for, request
import requests
import requests_cache
from dotenv import load_dotenv

from EmailSender import EmailSender

# Install a global cache -- delete requests-cache if you want a fresh query to the API endpoint
session = requests_cache.CachedSession('request-cache', expire_after=0)

# Create emailSender obj, get .env variables, send email
load_dotenv()

# API endpoint for the Blog
BLOG_ENDPOINT = "https://api.npoint.io/54c50cd63cc7f449e25f"

EMAIL = os.environ.get("EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# Create EmailSender obj
email_sender = EmailSender(email=EMAIL, password=GMAIL_APP_PASSWORD)

# Fetch the data from the API endpoint and render the posts on the homepage
response = session.get(url=BLOG_ENDPOINT)
print(f'Fetching request response from cache? {response.from_cache}')
posts = response.json()

# Map the image to the post_id
images = {
    1: "cactus.jpg",
    2: "dog_bored.jpg",
    3: "intermittent_fasting.jpg"
}

app = Flask(__name__)

@app.route('/')
def home_route():
    # Fetch the posts data
    return render_template('index.html', posts=posts)

@app.route('/about')
def show_about():
    return render_template('about.html')

@app.route('/contact', methods=["GET", "POST"])
def handle_contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        # Build email content, then send the email
        content = f"Name: {name}\n"\
              f"Email: {email}\n"\
              f"Phone: {phone}\n"\
              f"message: {message}\n"
        email_sender.send_email(content=content, from_addr=EMAIL, to_addr=EMAIL)

        return render_template('contact.html', welcome_msg=f"Successfully sent your message! Username: {name}")
    return render_template('contact.html', welcome_msg="Contact Me")

@app.route('/<post_id>')
def post_page(post_id):
    bg_img = images[int(post_id)]
    return render_template('post.html', post_id=int(post_id), posts=posts, bg_img=bg_img)

if __name__ == "__main__":
    app.run(debug=True)