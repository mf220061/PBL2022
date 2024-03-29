from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from auth import login_required
from db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/')
def index():
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    )
    posts = cursor.fetchall()
    cursor.close()
    #connection.close()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            connection = get_db()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO post (title, body, author_id)"
                " VALUES ('{}', '{}', '{}')".format(
                    title, body, g.user['id']
                )
            )
            connection.commit()
            cursor.close()
            #connection.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id = '{}'".format(id)
    )
    post = cursor.fetchone()
    cursor.close()
    #connection.close()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            connection = get_db()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "UPDATE post SET title = '{}', body = '{}' WHERE id = '{}'".format(title, body, id)
            )
            connection.commit()
            cursor.close()
            #connection.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM post WHERE id = '{}'".format(id))
    connection.commit()
    cursor.close()
    #connection.close()
    return redirect(url_for('blog.index'))
