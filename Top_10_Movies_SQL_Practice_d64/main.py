'''
    Application that lets me practice UPDATE, DELETE, ADD, and other SQLAlchemy operations on
    a "favorite movies" website. It also lets me practice using Flask-WTForms, and using APIs
    to pull data to present new info on the site (i.e., add movie).

    Requirements:
    1. Be able to view movie list items
    2. Edit a movie's rating and review (edit page)
    3. Delete Movies from the database (from index.html)
    4. Add new movies via the add page
    5. Sort and rank movies by rating.

    NOTE: The CSS file is missing and was too long to hard-copy over, so website looks jankey, but it's fully
    functional!
'''

import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import requests

# Load in env vars
load_dotenv()

# Constants loaded in -- for The Movie Database
API_READ_TOKEN = os.environ.get("API_READ_TOKEN")
API_KEY = os.environ.get("API_KEY")
API_BASE_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
API_MOVIE_DETAILS_ENDPOINT = "https://api.themoviedb.org/3/movie"
BASE_IMG_PATH = "https://image.tmdb.org/t/p/original"

# API headers
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_READ_TOKEN}"
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a;sldkfja;lskdjfe;lknv'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
Bootstrap5(app)

# Update movie form
class UpdateForm(FlaskForm):
    rating = FloatField(label='rating', validators=[DataRequired()])
    review = StringField(label='review', validators=[DataRequired()])
    done = SubmitField(label='done')

# New movie form
class NewMovieForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()])
    button = SubmitField(label='Add Movie')

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Movie(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[float] = mapped_column(Float, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# CREATE TABLE
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # new_entry = Movie(
    #     title = "Phone Booth",
    #     year = 2002,
    #     description = "This text is way too long, so I'm stopping here!",
    #     rating = 7.3,
    #     ranking = 10,
    #     review = "My favorite character was the caller (or so Angela Yu says!).",
    #     img_url = "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38z1ZM7Uc10.jpg"
    # )
    # db.session.add(new_entry)
    # db.session.commit()

    # new_entry = Movie(
    #     title = "Avatar The Way of Water",
    #     year = 2022,
    #     description = "This text is way too long, so I'm stopping here!",
    #     rating = 7.3,
    #     ranking = 9,
    #     review = "I liked the water(or so Angela Yu says!).",
    #     img_url = "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38z1ZM7Uc10.jpg"
    # )
    # db.session.add(new_entry)
    # db.session.commit()

    # Query the movies from the Movie table in the movies.db
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    movies = result.scalars().all()

    # Assign numbers (1,2,3...) to ranking in each movies by rating
    for i in range(len(movies)):
        movies[i].ranking = len(movies) - 1
    db.session.commit()

    return render_template("index.html", movies=movies)

@app.route('/edit', methods=["GET", "POST"])
def edit():
    # Create the form to show
    form = UpdateForm()
    movie_id = request.args.get('id')
    
    # Query the movie by the movie_id
    result = db.get_or_404(Movie, movie_id)
    movie = result

    # Update the fields for the movie; commit to db session
    if form.validate_on_submit():
        # Update the data in the database
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        # Return to the homepage to show updated results
        return redirect('/')

    return render_template('edit.html', movie=movie, form=form)

@app.route('/delete')
def delete():
    # Delete the movie by the id
    movie_id = request.args.get('id')
    db.session.delete(db.get_or_404(Movie, movie_id))
    db.session.commit()
    return redirect('/')

@app.route('/add', methods=["GET", "POST"])
def add():
    # Add a new movie by title
    form = NewMovieForm()

    # If we submitted the form
    if form.validate_on_submit():
        # Use an API to fetch the poster img, year of release, and movie description
        movie_title = form.title.data
        response = requests.get(url=API_BASE_ENDPOINT, headers=headers, params={"query": movie_title})
        response.raise_for_status()

        # Get the list[dict] containing the query search results
        q_results = response.json()['results']

        # Render the template with the q_results
        return render_template('select.html', results=q_results)

    return render_template('add.html', form=form)

@app.route('/find')
def find_movie():
    ''' Find the movie by id and get its details. '''
    # Add a movie if movie_id is set
    movie_id = request.args.get('movie_id')

    if movie_id != None:
        response = requests.get(url=f'{API_MOVIE_DETAILS_ENDPOINT}/{movie_id}', headers=headers)
        response.raise_for_status()

        result = response.json()

        # Get release date, title, img_url, and description
        new_movie = Movie(
            description = result['overview'],
            img_url = f"{BASE_IMG_PATH}{result['poster_path']}",
            title = result['title'],
            year = result['release_date'].split("-")[0]
        )

        # Add it to the database
        db.session.add(new_movie)
        db.session.commit()

        # Get the primary key id from the new entry that was inserted
        id = new_movie.id #db.session.execute(db.select(Movie).where(Movie.title == result['title'])).id
        return redirect(url_for('edit', id=id))

if __name__ == "__main__":
    app.run(debug=True)