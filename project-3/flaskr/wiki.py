from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, send_from_directory)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('wiki', __name__)


@bp.route('/')
def index():
    db = get_db()
    articles = db.execute(
        'SELECT p.id, title, body, created, author_id, username, summary, img'
        ' FROM article p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('wiki/index.html', articles=articles)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        # update when template is modified
        title = request.form['title']
        body = request.form['body']
        summary = request.form['summary']

        f = request.files['file']
        filename = secure_filename(f.filename)
        if not filename:
            filename = 'DEFAULT.jpg'
        up = f"{bp.root_path}/static/Uploads/{filename}"
        f.save(up)

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO article (title, summary, body, author_id, img)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, summary, body, g.user['id'], filename)
            )
            db.commit()
            return redirect(url_for('wiki.index'))

    return render_template('wiki/create.html')


def get_article(id, check_author=True):
    article = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, summary, img'
        ' FROM article p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if article is None:
        abort(404, f"Article id {id} doesn't exist.")

    if check_author and article['author_id'] != g.user['id']:
        abort(403)

    return article


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    article = get_article(id)

    if request.method == 'POST':
        # need to include summary and img
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE article SET title = ?, body = ?, summary = ?, img = ?'
                ' WHERE id = ?',
                (title, body, "summary_ph", "img_ph", id)
            )
            db.commit()
            return redirect(url_for('wiki.index'))

    return render_template('wiki/update.html', article=article)

# Detail view


@bp.route('/<int:id>', methods=('GET',))
@login_required
def detail(id):
    article = get_article(id, check_author=False)
    db = get_db()
    comments = db.execute(
        'SELECT comment.id, body, created, author_id, username'
        ' FROM comment JOIN user ON author_id = user.id'
        ' WHERE article_id = ?',
        str(id)
    ).fetchall()
    return render_template('wiki/detail.html', art=article, comments=comments)

# ----------- Comment


@bp.route('/create_comment/<int:id>', methods=('POST', 'GET'))
@login_required
def create_comment(id):
    if request.method == 'POST':
        body = request.form['body']

        if not body:
            flash('Comment body is required.', 'error')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO comment (article_id, author_id, body)'
                ' VALUES (?, ?, ?)',
                (id, g.user['id'], body)
            )
            db.commit()
        flash('Comment created successfully!')
        # change to return to article view
        return redirect(url_for('wiki.detail', id=id))
    return render_template('wiki/create_comment.html')

# ----------- Delete


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_article(id)
    db = get_db()
    db.execute('DELETE FROM article WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('wiki.index'))


'''
# ----------- Image Upload
@bp.route('/upload', methods=('GET', 'POST'))
def image_upload():
    up = None
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        up = f"{bp.root_path}/static/Uploads/{filename}"
        f.save(up)
        return render_template()
    return render_template('wiki/uploaded.html', filename=f.filename)
'''


@bp.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(f"{bp.root_path}/static/Uploads", filename)
