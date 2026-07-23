'''
    Class that implements a simple LoginForm for use in today's exercises.
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField(label='email', validators=[DataRequired()])
    password = PasswordField(label='password', validators=[DataRequired()])
    login_button = SubmitField(label='Log In')