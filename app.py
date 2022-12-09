"""Blogly application."""
from models import User, db, connect_db
from flask import Flask, request, render_template, redirect, flash, session


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """Shows home page"""
    users = User.query.all()
    return render_template('home.html', users=users)



@app.route("/", methods=["POST"])
def add_pet():
    """Add pet and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    url = request.form['url']

    new_user = User(first_name=first_name, last_name=last_name, url=url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/{new_user.id}")

@app.route("/<int:user_id>")
def show_pet(user_id):
    """Show info on a single pet."""

    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user.id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")