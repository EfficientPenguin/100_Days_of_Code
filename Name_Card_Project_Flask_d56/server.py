
'''
    Simple Flask application to practice rendering templates (i.e., HTML files and their CSS)
'''

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_route():
    return render_template('index.html', name=None)

if __name__ == "__main__":
    app.run(debug=True)