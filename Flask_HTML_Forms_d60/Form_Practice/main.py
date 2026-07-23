'''
    The goal of today's lesson is to learn about how HTML forms are filled out using Flask, and to send an email once
    the button to submit the info on the forms is pressed.
'''

import smtplib
from flask import Flask, render_template, request

def add_h1(function):
    def wrap():
        return f"<h1>{function()}</h1>"
    return wrap

app = Flask(__name__)

@app.route('/')
def homepage():
    ''' Display the contents of the homepage.'''
    return render_template('index.html')

@app.route('/login', methods=["POST"])
@add_h1
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    return f"Name: {username},Password: {password}"
    #return "💪 Success! Form submitted"

if __name__ == "__main__":
    app.run(debug=True)