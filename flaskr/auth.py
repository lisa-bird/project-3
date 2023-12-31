import functools
import psycopg2
from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# ---- Register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                cursor = db.cursor()
                cursor.execute(
                    'INSERT INTO "user" (username, password) VALUES (%s, %s)',
                    (username, generate_password_hash(password)),
                )
                cursor.close()
                db.commit()
            except psycopg2.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


# ---- Login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'  
        
        if error is None:
            try:
                cursor = db.cursor()
                cursor.execute(
                    'SELECT * FROM "user" WHERE username = %s',
                    (username,),
                )
                user = cursor.fetchone()

                if user is None:
                    error = 'Incorrect username.'
                elif not check_password_hash(user[2], password):
                    error = 'Incorrect password.'

                cursor.close() 

                if error is None:
                    session.clear()
                    session['user_id'] = user[0]
                    return redirect(url_for('index'))

            except psycopg2.Error as e:
                error = f'Database error: {e}'

        flash(error)

    return render_template('auth/login.html')   


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT * FROM "user" WHERE id = %s', 
            (user_id,)
        )
        g.user = cursor.fetchone()
        cursor.close()


# ---- Logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
