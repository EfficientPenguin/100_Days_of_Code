'''
    Simple and minimal Flask app.
'''

from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bye')
def print_bye():
    return 'Bye bye!'

if __name__ == "__main__":
    app.run()