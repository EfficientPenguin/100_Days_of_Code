'''
    Application to test SQLAlchemy code compared to sqlite3. SQLAlchemy is an ORM, so it's much less error-prone.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

# CHALLENGE

# 1. Init the db object
# 2. Define your model
# 3. Create the table

class Books(DeclarativeBase):
    # ID, TITLE, AUTHOR, RATING
    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(nullable=False, unique=True)
    author : Mapped[str] = mapped_column(nullable=False)
    title : Mapped[float] = mapped_column(nullable=False)

db = SQLAlchemy(model_class=Books)