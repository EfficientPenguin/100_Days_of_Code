'''
    Flask application that lets me practice advanced decorators, embedding HTML and CSS into return strings,
    using variable_names with converters to specify data types, and more. Corresponds to Day 55.
'''

from flask import Flask

def make_bold(function):
    def wrapper_function():
        return f'<b>{function()}</b>'
    return wrapper_function

def make_emphasis(function):
    def wrapper_function():
        return f'<em>{function()}</em>'
    return wrapper_function

def make_underlined(function):
    def wrapper_function():
        return f'<u>{function()}</u>'
    return wrapper_function

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Variable name in <> brackets
@app.route('/username/<name>')
def print_username(name):
    return f'Hello {name} updated code!'

# Variable name with a converter applied to specify data type
@app.route('/<int:number>')
def print_if_number(number):
    if type(number) == int:
        return f"User provided a number. The number is {number}"
    
# Variable name with HTML tags and CSS inline styles applied
@app.route('/html_data')
def render_as_html():
    return '<h1 style="text-align: center">Hello, World!</h1>'\
            '<p>Im a paragraph!</p>'\
            '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjV0eGN6ams4eXNwbW5oM2tsY3hvZXA3M2tmZjVmNDNoZDg5ZWF2aSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/j93ycvEyWlSIIg8AEl/giphy.gif">'

# Challenge: Add decorators to apply bold, italic, and underlined HTML tags to the return text of bye
@app.route('/bye')
@make_bold
@make_emphasis
@make_underlined
def bye():
    return "Bye!"

if __name__ == "__main__":
    app.run(debug=True)