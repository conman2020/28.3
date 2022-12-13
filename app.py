"""Blogly application."""
from models import User, Post, db, connect_db
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
def users_updated(user_id):
    """Handle form submission for updating an existing user"""

    newest_user = User.query.get_or_404(user_id)
    newest_user.first_name = request.form['first_name']
    newest_user.last_name = request.form['last_name']
    newest_user.url = request.form['url']

    db.session.add(newest_user)
    db.session.commit()

    return redirect("/")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route('/users/<int:user_id>/newpost')
def users_new_post(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/newpost.html', user=user)

@app.route('/users/<int:user_id>/newpost', methods=["POST"])
def users_new_posted(user_id):
    """Handle form submission for updating an existing user"""

    user_id = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect("/")


@app.route("/posts/<int:post_id>")
def show_specific_post(post_id):
    """Show info on a single pet."""

    post = Post.query.get_or_404(post_id)
    return render_template("/posts/edit.html", post=post)

@app.route("/users/<int:user_id>")
def go_back_to_user(user_id):
    """Show info on a single pet."""

    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)
@app.route("/posts/<int:post_id>/change")
def load_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/change.html', post=post)


@app.route("/posts/<int:post_id>/change", methods=["POST"])
def edit_form(post_id):
    changed_post = Post.query.get_or_404(post_id)
    changed_post.title = request.form['title']
    changed_post.content = request.form['content']

    db.session.add(changed_post)
    db.session.commit()

    return redirect("/")



@app.route('/users/<int:user_id>/delete', methods=["POST"])
def form_delete(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")