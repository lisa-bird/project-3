from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, send_from_directory)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
import psycopg2

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('wiki', __name__)


# ---- Index view
@bp.route('/')
def index():
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        'SELECT a.id, a.title, a.created, a.author_id, u.username, a.summary, a.img, COUNT(c.id) AS comment_count '
        'FROM article a '
        'LEFT JOIN "user" u ON a.author_id = u.id '
        'LEFT JOIN comment c ON a.id = c.article_id '
        'GROUP BY a.id, a.title, a.created, a.author_id, u.username, a.summary, a.img '
        'ORDER BY a.created DESC'
    )

    
    articles = cursor.fetchall()
    # Get the column names from cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Iterate through the rows and map them to dictionaries
    article_list = []
    for row in articles:
        row_dict = dict(zip(column_names, row))
        article_list.append(row_dict)

    cursor.close()  
    print(f">>>{article_list}")
    return render_template('wiki/index.html', articles=article_list)


# ---- Create View
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':        
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
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO article (title, summary, body, author_id, img)'
                ' VALUES (%s, %s, %s, %s, %s )',
                (title, summary, body, g.user[0], filename)
            )
            db.commit()
            cursor.close()

            return redirect(url_for('wiki.index'))

    return render_template('wiki/create.html')


def get_article(id, check_author=True):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT p.id, title, body, created, author_id, username, summary, img'
        ' FROM article p JOIN "user" u ON p.author_id = u.id'
        ' WHERE p.id = %s',
        (id,)
    )
    article = cursor.fetchone()

    column_names = [desc[0] for desc in cursor.description]

    article = dict(zip(column_names,article))

    cursor.close()

    if article is None:
        abort(404, f"Article id {id} doesn't exist.")

    if check_author and article['author_id'] != g.user[0]:
        abort(403)

    return article


# ---- Update view
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    article = get_article(id)

    if request.method == 'POST':        
        title = request.form['title']
        body = request.form['body']
        summary = request.form['summary']
        img = article['img']
        print(f"UPDATE>image name used is {img}")
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'UPDATE article SET title = %s, body = %s, summary = %s, img = %s'
                ' WHERE id = %s',
                (title, body, summary, img, id)
            )
            db.commit()
            cursor.close()
            return redirect(url_for('wiki.index'))

    return render_template('wiki/update.html', article=article)


# ---- Detail view
@bp.route('/<int:id>', methods=('GET',))
@login_required
def detail(id):

    article = get_article(id, check_author=False)
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT comment.id, body, created, author_id, username'
        ' FROM comment JOIN "user" ON author_id = "user".id'
        ' WHERE article_id = %s',
        (str(id),)
    )
    comments = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
   
    comment_list = []
    for row in comments:
        row_dict = dict(zip(column_names, row))
        comment_list.append(row_dict)

    cursor.close()    
    return render_template('wiki/detail.html', art=article, comments=comment_list)


# ---- Create comment view
@bp.route('/create_comment/<int:id>', methods=('POST', 'GET'))
@login_required
def create_comment(id):
    if request.method == 'POST':
        body = request.form['body']

        if not body:
            flash('Comment body is required.', 'error')
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO comment (article_id, author_id, body)'
                ' VALUES (%s, %s, %s)',
                (id, g.user[0], body)
            )
            db.commit()
            cursor.close()
        flash('Comment created successfully!')        
        return redirect(url_for('wiki.detail', id=id))
    return render_template('wiki/create_comment.html')


# ---- Delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_article(id)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM article WHERE id = %s', (id,))
    db.commit()
    cursor.close()
    return redirect(url_for('wiki.index'))


# ---- Upload
@bp.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(f"{bp.root_path}/static/Uploads", filename)
