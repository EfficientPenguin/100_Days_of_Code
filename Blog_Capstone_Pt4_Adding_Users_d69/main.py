
'''
    Capstone Project for Day 69. It adds RESTful routing to Pt3's Day 67 Blog Capstone project.
    Requirements:
        1. Register New Users
        2. Login Registered Users
        3. Protect Routes
        4. Create relational databases
        5. Allow any user to add comments to BlogPosts
'''
from datetime import date
from typing import List

from sqlalchemy import ForeignKey
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# TODO: Configure Flask-Login
# Init loginManager and set a SECRET_KEY
app.secret_key = 'asd;lfkjeoijDKJLFL:J'
login_manager = LoginManager()
login_manager.init_app(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    ''' One to many relationship between BlogPost (Parent) and Comment (child). Each BlogPost can have many Comment
    objects. One to many relationship between '''
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # Create reference to the User object. The "posts" refers to the posts property in the User class.
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # Create Foreign Key, "users.id" the users refres to the tablename of User.
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="parent_post")


# TODO: Create a User table for all your registered users. 
class User(UserMixin, db.Model):
    ''' One to many relationship between the User table (Parent) and Comment table (Child). One User is linked to Many
    Comment objects.
    '''
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="author")

# Comment table to hold comments for each post
class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author = relationship("User", back_populates="comments")

    post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")

with app.app_context():
    db.create_all()

# Decorators to protect unwanted editing/deleting of posts
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.id != 1:
            # If not admin user, then return 403 error
            return abort(403)
        return func(*args, **kwargs)
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        name = register_form.name.data
        email = register_form.email.data

        # Check if email already exists (i.e., user is trying to register twice!)
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user:
            flash('That email is already registered! Please log in.')
            return redirect(url_for('login'))
        
        # Add the user to the database
        new_user = User(
            name = name,
            email = email,
            password = generate_password_hash(register_form.password.data, method='pbkdf2:sha256', salt_length=8)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=register_form)


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Verify the login is correct
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user:
            # Check the password in db against user-provided password
            if check_password_hash(user.password, password):
                # Login the user
                login_user(user)
                return redirect(url_for('get_all_posts'))
            flash('Incorrect password. Please try again.')
            return redirect(url_for("login"))
        flash('Invalid email. Please try again.')
        return redirect(url_for("login"))
    
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/', methods=["GET"])
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", 
                           all_posts=posts, 
                           logged_in=current_user.is_authenticated, 
                           is_admin=True if current_user.get_id() == "1" else False)

# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You must be logged in to comment! Please log in.')
            return redirect(url_for('login'))
        comment = Comment(
            text = form.comment.data,
            author_id = current_user.id,
            post_id = post_id
        )
        db.session.add(comment)
        db.session.commit()
    return render_template("post.html", post=requested_post, logged_in=current_user.is_authenticated, form=form)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author_id=current_user.id,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, logged_in=current_user.is_authenticated)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id), is_admin=True if current_user.id == 1 else False)
    return render_template("make-post.html", form=edit_form, is_edit=True, logged_in=current_user.is_authenticated)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route("/contact")
def contact():
    return render_template("contact.html", logged_in=current_user.is_authenticated)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
