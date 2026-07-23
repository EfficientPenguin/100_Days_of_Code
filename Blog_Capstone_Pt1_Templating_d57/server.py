
'''
    Simple Flask application to practice templating using Jinja.
'''

import random
import datetime as dt

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_route():
    random_number = random.randint(0,9)
    return render_template("index.html", num=random_number, curr_year=dt.datetime.today().year)

if __name__ == "__main__":
    app.run(debug=True)