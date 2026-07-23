
'''
    Simple Flask application that shows a Name card using a template. I just used Angela Yu's picture instead of my
    own as this is educational only. Template for the site for HTML/CSS and JS can be found here: https://html5up.net/.
    The theme used was called "Highlights".
'''

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_route():
    return render_template('index.html', name=None)

if __name__ == "__main__":
    app.run(debug=True)