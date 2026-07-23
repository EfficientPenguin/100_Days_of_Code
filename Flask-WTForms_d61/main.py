'''
    This day introduces "Flas-WTForms" which allows for easier HTML form control and validation and overall
    less code. It is the preferred way Flask developers use HTML forms.
'''

from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, url_for, request, redirect

from LoginForm import LoginForm

def validate_credentials(email: str, password: str) -> bool:
    ''' Validate the credentials provided/submitted in the form on the login page.'''
    if email != "admin@email.com":
        return False
    if password != "12345678":
        return False
    return True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secure-secret-key' # Required for CSRF

bootstrap = Bootstrap5(app)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    # Create a loginForm obj
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if validate_credentials(email=login_form.email.data, password=login_form.password.data):
            return render_template('success.html')
        return render_template('denied.html')
    return render_template('login.html', form=login_form)

if __name__ == "__main__":
    app.run(debug=True)