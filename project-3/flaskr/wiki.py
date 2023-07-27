from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

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
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO article (title, summary, body, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, "placeholder", body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('wiki.index'))

    return render_template('wiki/create.html')


def get_article(id, check_author=True):
    article = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, summary, img'
        ' FROM post p JOIN user u ON p.author_id = u.id'
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


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_article(id)
    db = get_db()
    db.execute('DELETE FROM article WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('wiki.index'))
