
'''
    Capstone Project for Day 67. It adds RESTful routing to Pt2's Day 59 Blog Capstone project.
    Requirements:
        1. Be able to GET Blog Post Items
        2. Be Able to POST a New Blog
        3. Be able to Edit Exisitng Blog Post
        4. Be able to DELETE Blog Posts
'''

from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

from datetime import date

app = Flask(__name__)
app.config["SECRET_KEY"] = "DOIJ93089FKLJsdflkj#@;lkj"
Bootstrap5(app)

# Create DB
class Base(DeclarativeBase):
    pass
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CKEditor initialization
app.config['CKEDITOR_PKG_TYPE'] = 'basic'  # Options: basic, standard, full
ckeditor = CKEditor(app)

# Configure Table
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# Flask Form for new post using CKEditor for rich text 'body' text area
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    img_url = StringField('Blog Image URL', validators=[DataRequired()])
    body = CKEditorField('Blog Content', validators=[DataRequired()])
    submit = SubmitField('Submit Post')

with app.app_context():
    db.create_all()

@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)

# Add a route so that you can click on individual posts
@app.route('/show_post')
def show_post():
    # TODO: Retrieve a BlogPost form the database based on the post_id
    post_id = request.args.get('post_id')
    requested_post = db.session.get(BlogPost, post_id)
    return render_template("post.html", post=requested_post)

# add_new_post() to create a new blog post
@app.route('/new-post', methods=["GET", "POST"])
def add_new_post():
    ''' Add a new post by having user fill out a form with the details.'''
    form = PostForm()

    if form.validate_on_submit():
        # Add the new post to the database
        new_post = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            author = form.author.data,
            img_url = form.img_url.data,
            body = form.body.data,
            date = date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=form, is_edit=False)

# edit_post() to change an existing blog post
@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    ''' Edit an existing post.'''
    # Prepopulate the form with the data from the db
    post = db.get_or_404(BlogPost, post_id)
    edit_form = PostForm(
        title = post.title,
        subtitle = post.subtitle,
        author = post.author,
        img_url = post.img_url,
        body = post.body,
        date = post.date
    )

    if edit_form.validate_on_submit():
        # Edit the fields of the post and commit to the database
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.author = edit_form.author.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        # post.date = date.today().strftime("%B %d, %Y")
        db.session.commit()

        return redirect(url_for('get_all_posts'))

    return render_template('make-post.html', form=edit_form, is_edit=True)


# delete_post() to remove a blog post form the database
@app.route('/delete/<int:post_id>', methods=["GET"])
def delete_post(post_id):
    ''' DELETE a post. '''
    # Select the post in the db
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('get_all_posts'))



# Below is the code from previous lessons. No changes needed.
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)