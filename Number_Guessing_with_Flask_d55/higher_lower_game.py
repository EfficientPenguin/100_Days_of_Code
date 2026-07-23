'''
    Flask application that implements a simple number guessing game using URL typing of the user
    and displaying different web pages.
'''

import random

from flask import Flask

# Cat gifs
num_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXI1OXd5ZHp3OTQ3dXI2aHpjeXljY3R0eW41cG5hZ3U3d2picWh2NSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/LfbDxyQIWtzLTtMnc0/giphy.gif"
cat_gif_looking_up = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjV0eGN6ams4eXNwbW5oM2tsY3hvZXA3M2tmZjVmNDNoZDg5ZWF2aSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/0oIkdy76oYE8uPsPjy/giphy.gif"

# Generate the random number between 1 and 9
num_to_guess = random.randint(1,9)

# Functions to apply images and other decorators
def apply_h1(function):
    def wrapper():
        return f'<h1>{function()}</h1>'
    return wrapper

def home_page_gif(function):
    def wrap():
        return f'{function()}<br><img src={num_gif}>'
    return wrap


app = Flask(__name__)

@app.route('/')
@apply_h1
@home_page_gif
def home_route():
    return 'Guess a number between 1 and 9'

@app.route('/<int:number>')
def handle_guess(number):
    if number > num_to_guess:
        return f'<h1 style="color: purple">{number} is too high, bruh! Try again</h1><br><img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmJnOHUweWRnbWtkMzJkc2Z6OWw5aWN0MDdxMmFzcmVuODU2eTdicSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/baNxGhmywafa3h7gPr/giphy.gif">'
    elif number < num_to_guess:
        return f'<h1 style="color: red">{number} is too low, waaaaah! Try again</h1><br><img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHkxNG5zMzV5dTFqczRtMmYwNG9hYTl4dXgzd2cxMmp1eGViOTc0eiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/EQIkgfMCjs1kk/giphy.gif">'
    return f'<h1 style="color: green">congrats! you got it! The number was {number}.</h1><br><img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTJ5MmJud2libDFpb240MXQ5eWpzbzdncmgxZDFibXdmOG56bWVhdCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/B0vFTrb0ZGDf2/giphy.gif">'

if __name__ == "__main__":
    app.run(debug=True)