
'''
    Capstone Project from Day 59: Add styling to the Blog project from Day 56. Practice using
    Bootstrap templates to achieve the desired result. Add a link called
    "Read" that will provide the "body" of the blog on a page given by its id: URL/post/blog_id.
    The URL/post page should only list the "title" and "subtitle" fields.
'''

from flask import Flask, render_template, url_for
import requests

# API endpoint for the Blog
BLOG_ENDPOINT = "https://api.npoint.io/54c50cd63cc7f449e25f"

# Fetch the data from the API endpoint and render the posts on the homepage
response = requests.get(url=BLOG_ENDPOINT)
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

@app.route('/contact')
def show_contact():
    return render_template('contact.html')

@app.route('/<post_id>')
def post_page(post_id):
    bg_img = images[int(post_id)]
    return render_template('post.html', post_id=int(post_id), posts=posts, bg_img=bg_img)

if __name__ == "__main__":
    app.run(debug=True)