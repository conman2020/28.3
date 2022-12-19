"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import  Integer, DateTime
db = SQLAlchemy()
DEFAULT_IMG= "https://www.freeiconspng.com/img/49570"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ ="users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    url = db.Column(db.Text,nullable=False, default=DEFAULT_IMG)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


class Post(db.Model):
    """Department. A department has many employees."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                          nullable=False,
                          unique=True)
    content = db.Column(db.Text)
    created_at=db.Column(db.DateTime,nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))




class Tag(db.Model):
    __tablename__= "tags"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False)
    posts = db.relationship(
        'Post',
        secondary="posttags",
        cascade="all,delete",
        backref="tags"
    )
    

class PostTag(db.Model):
    __tablename__= "posttags"
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)