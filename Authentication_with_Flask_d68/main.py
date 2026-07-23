'''
    Day 68 focuses on Advanced Authentication with Flask. The application can:
        1. Register New Users
        2. Hashing and Salting passwords using Werkzeug
        3. Authenticating users using Flask-Login
        4. Flask Flash Messages
        5. Passing Authentication Status to Templates

    The 'secrets' page is only accessible if the user is logged in.
'''

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "asdlfkj;l398948985KJ:LKJ"

# Init loginManager and set a SECRET_KEY
app.secret_key = 'asd;lfkjeoijDKJLFL:J'
login_manager = LoginManager()
login_manager.init_app(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create table in DB
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get the form data
        form_name = request.form['name']
        form_email = request.form['email']

        # Check if the user already exists in the db
        result = db.session.execute(db.select(User).where(User.email == form_email))
        user = result.scalar()

        if user:
            # Redirect to the login page
            flash(f'User with email: {form_email} already registered. Please sign in.')
            return render_template('login.html', email=form_email)
        
        # Create a new User entry
        new_user = User(
            name = form_name,
            email = form_email,
            password = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
        )

        # Add and commit new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log in and authenticate user after adding details to database.
        login_user(new_user)

        # Can redirect() and get name from the current_user
        return redirect(url_for("secrets"))

    return render_template("register.html", logged_in=current_user.is_authenticated)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Get user by email
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user:
            # Check stored password hash against entered password hashed.
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('secrets'))
            flash("Password incorrect. Please try again.")
            return render_template("login.html", email=email)
        flash("That email doesn't exist. Please try again.")
        return render_template("login.html", email=email)

    return render_template("login.html", email=None, logged_in=current_user.is_authenticated)

@app.route('/secrets')
@login_required
def secrets():
    # Pass the name from the current_user
    return render_template("secrets.html", name=current_user.name, logged_in=True)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory('static', path='files/cheat_sheet.pdf')

if __name__ == "__main__":
    app.run(debug=True, port=5003)