#import statements
import os
import sqlite3
from flask import (Flask, request, session, g, redirect, url_for, abort,
render_template, flash)

app = Flask(__name__) #create application instance
app.config.from_object(__name__) #load config from this file, flaskr.py


#load default configuration and override configuration from an environment variable
app.config.update( 
    DATABASE = os.path.join(app.root_path, 'flaskr.db'), #used to get the path to the application
    SECRET_KEY = 'hard-to-guess',
    USERNAME = 'admin123',
    PASSWORD = 'admin123'
)

#connection to the database
#uses SQLite database
def connect_db():
    """connects to the specific database"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row 
    return rv

def init_db():
    db = get_db()

    with app.open_resource('schema.sql', mode='r' ) as f:
        db.cursor().executescript(f.read())

    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """initializes the database"""

    init_db()
    print('Initialized the database')

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    return "Error"

@app.route('/') 
def show_entries(): 
    db = get_db() 
    cur = db.execute('select title, text from entries order by id desc') 
    entries = cur.fetchall() 
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
    [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was succesfully posted')
    return redirect(url_for('show_entries'))


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
            flash('You are logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))





