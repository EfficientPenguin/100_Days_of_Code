'''
    Day 62 dealt with starting from a base project, then using Flask, Flask-WTForms, Bootstrap-Flask, build the website
    to the desired spec. It involved loading in CSS and JS using bootstrap flask, using Jinja templating to build
    the Boostrap table, using Flask-WTForms to create the forms on the /add page, and using CSV read/write to read/write
    and display data on the /cafes page.
'''

from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'as;ldkfja;lskjdflkjlkjelf'
Bootstrap5(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL()])
    open_time = StringField('Open Time', validators=[DataRequired()])
    close_time = StringField('Close Time', validators=[DataRequired()])
    coffee = SelectField('Coffee rating', choices=[('☕️', '☕️'),
                                                    ('☕️☕️', '☕️☕️'),
                                                    ('☕️☕️☕️', '☕️☕️☕️'),
                                                    ('☕️☕️☕️☕️', '☕️☕️☕️☕️'),
                                                    ('☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️')])
    wifi = SelectField('Wifi rating', choices=[('💪', '💪'),
                                                    ('💪💪', '💪💪'),
                                                    ('💪💪💪', '💪💪💪'),
                                                    ('💪💪💪💪', '💪💪💪💪'),
                                                    ('💪💪💪💪💪', '💪💪💪💪💪')])
    power = SelectField('Power rating', choices=[('🔋', '🔋'),
                                                    ('🔋🔋', '🔋🔋'),
                                                    ('🔋🔋🔋', '🔋🔋🔋'),
                                                    ('🔋🔋🔋🔋', '🔋🔋🔋🔋'),
                                                    ('🔋🔋🔋🔋🔋', '🔋🔋🔋🔋🔋')])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# eg., you could use emojis
# make all fields required except submit
# use a validator to check that the URL field has a URL entered
# ----------------------------

# all flask routes below
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        # Exercise:
        # Make the form write a new row into cafe-data.csv
        # with if form.validate_on_submit()
        # Get the data for each and make it a list
        form_data = [
            form.cafe.data,
            form.location.data,
            form.open_time.data,
            form.close_time.data,
            form.coffee.data,
            form.wifi.data,
            form.power.data
        ]
        with open('cafe-data.csv', newline='', encoding='utf-8', mode='a') as csv_file:
            csv_data = csv.writer(csv_file, delimiter=',')
            csv_data.writerow(form_data)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

@app.route('/cafes', methods=["GET", "POST"])
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        
    return render_template('cafes.html', cafes=list_of_rows)

if __name__ == "__main__":
    app.run(debug=True)