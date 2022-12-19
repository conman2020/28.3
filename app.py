"""Blogly application."""
from models import User, Post, PostTag, Tag, db, connect_db
from flask import Flask, request, render_template, redirect, flash, session


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'mysecret'

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

@app.route("/users/<int:user_id>")
def go_back_to_user(user_id):
    """Show info on a single pet."""

    user = User.query.get_or_404(user_id)

    return render_template("details.html", user=user)

@app.route('/users/<int:user_id>/edituser')
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edituser.html', user=user)

@app.route('/users/<int:user_id>/edituser', methods=["POST"])
def users_updated(user_id):
    """Handle form submission for updating an existing user"""

    newest_user = User.query.get_or_404(user_id)
    newest_user.first_name = request.form['first_name']
    newest_user.last_name = request.form['last_name']
    newest_user.url = request.form['url']

    db.session.add(newest_user)
    db.session.commit()

    return redirect("/")
@app.route('/users/<int:user_id>/deleteuser', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

# Posts section
# efefe
# effefe
# effefef
# fefefe
# effefe




@app.route('/users/<int:user_id>/newpost')
def users_new_post(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    # posts = Post.query.get_or_404(post_id)
    return render_template('users/newpost.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/newpost', methods=["POST"])
def users_new_posted(user_id):
    """Handle form submission for updating an existing user"""

    user_id = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user=user_id,tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect("/")


@app.route("/posts/<int:post_id>")
def show_specific_post(post_id):
    """Show info on a single pet."""

    post = Post.query.get_or_404(post_id)
    return render_template("/posts/displaypost.html", post=post)


@app.route("/posts/<int:post_id>/changepost")
def load_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/changepost.html', post=post, tags=tags)


@app.route("/posts/<int:post_id>/changepost", methods=["POST"])
def edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    # user=post.user_id

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{Post.title}' edited.")
    return redirect(f"/users/{post.user_id}")
    # return render_template ("details.html", user=user)
    # post = Post.query.get_or_404(post_id)
    # post.title = request.form['title']
    # post.content = request.form['content']
    # tag_ids = [int(num) for num in request.form.getlist("tags")]
    # tag = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    # new_post = Post(title=post.title, content=post.content, user=user_id,tags=tag)

    # # title = request.form['title']
    # # content = request.form['content']
    # # tag_ids = [int(num) for num in request.form.getlist("tags")]
    # # tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    # # new_post = Post(title=title, content=content, user=user_id,tags=tags)

    # db.session.add(new_post)
    # db.session.commit()

    # return redirect("/")



@app.route('/users/<int:user_id>/delete', methods=["POST"])
def form_delete(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


# Tags section
# efefe
# effefe
# effefef
# fefefe
# effefe



@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/newtag')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/newtag.html', post=posts)


@app.route("/tags/newtag", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.post_id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, post=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.post_id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")