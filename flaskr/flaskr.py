# coding: utf-8
"""
    Flaskr
    ~~~~~~~~~~~~~
    A microblog example
"""
import os
import yaml
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g, render_template
from utils import logging

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY="xuejiao",
    USERNAME="admin",
    PASSWORD="default",
    ))
app.config.from_envvar("FLASKR_SETTINGS", silent=True)
logging.debug('in flaskr')

def init_db():
    """Initialize the db"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    """Open a new database connection if there is none yet
    for the current app context
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def connect_db():
    """Connect to specific db"""
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


@app.cli.command('initdb')
def initdb_command():
    """create the db tables"""
    init_db()
    logging.info('Initialized the database')

@app.teardown_appcontext
def close_db(error):
    """Closes the db again at the end of the request"""
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
