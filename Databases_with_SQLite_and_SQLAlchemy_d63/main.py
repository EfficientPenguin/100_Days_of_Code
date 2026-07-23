'''
    Today's goal is to learn about SQLite and SQLAlchemy and hook it up to Flask.
'''

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

# Define a Base class for SQLAlchemy
class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

# Create the db object using the SQLAlchemy constructor
db = SQLAlchemy(model_class=Base)

# Init the flask app with the Flask-SQLAlchemy extension:
db.init_app(app)

# Create a database table model
class Book(db.Model):
    # ID, TITLE, AUTHOR, RATING
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    author : Mapped[str] = mapped_column(String(250), nullable=False)
    rating : Mapped[float] = mapped_column(Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed
    def __repr__(self):
        return f'<Book {self.title}'

# After all models and tables are defined, call the following to create the tables:
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    id = request.args.get('id')
    if id != None:
        # Delete the entry
        row = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        db.session.delete(row)
        db.session.commit()
        redirect('home')
    # Read all the books to render
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return render_template('index.html', all_books=all_books)

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Create the new SQLAlchemy database entry in the Book table
        book = Book(
            title = request.form["title"],
            author = request.form["author"],
            rating = request.form["rating"]
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # Get the data from the textbox to update the request
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))
    # Get the ID passed from the index page
    id = request.args.get('id')

    # Get the data to display on the page by book id
    result = db.session.execute(db.select(Book).where(Book.id == id))
    book = result.scalar()

    return render_template('edit-rating.html', book=book)

if __name__ == "__main__":
    app.run(debug=True)