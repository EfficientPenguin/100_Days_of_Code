
'''
    Capstone Project from Day 56: Fetch the blogs from the blog API. Add a link called
    "Read" that will provide the "body" of the blog on a page given by its id: URL/post/blog_id.
    The URL/post page should only list the "title" and "subtitle" fields.
'''

from flask import Flask, render_template, url_for
import requests

# API endpoint for the Blog
BLOG_ENDPOINT = "https://api.npoint.io/c790b4d5cab58020d391"

app = Flask(__name__)

@app.route('/')
def home_route():
    # Fetch the posts data
    response = requests.get(BLOG_ENDPOINT)
    posts = response.json()
    return render_template('capstone_index.html', posts=posts)

@app.route('/post/<int:blog_id>')
def get_blog_content(blog_id):
    ''' Get the blog content by id from the list of posts'''
    response = requests.get(BLOG_ENDPOINT)
    blog_post = response.json()[blog_id-1]
    return render_template('post.html', blog_id=blog_id, blog_post=blog_post)

if __name__ == "__main__":
    app.run(debug=True)