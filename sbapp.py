# -*- coding: utf-8 -*-
"""
    sbapp backend
"""

import os
import time
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'DATABASE.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('config/init_database.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def success(result):
    return jsonify({"status":1, "data":result})


def fail(reason):
    return jsonify({"status":0, "data":reason})


@app.route('/sbapp/1.0/accounts')
def show_accounts():
    entries = None
    try:
        entries = query_db('select * from accounts')
    except Exception, e:
        return fail(str(e))
    return success(entries)


@app.route('/sbapp/1.0/add_account', methods=['POST'])
def add_account():
    db = get_db()
    print request
    try:
        db.execute('insert into accounts (username, password, phone, realname, gender, age, job) values (?, ?, ?, ?, ?, ?, ?)', [request.form['username'], request.form['password'], request.form['phone'], request.form['realname'], request.form['gender'], request.form['age'], request.form['job']])
        db.commit()
        account = query_db('select * from  accounts where username=?', [request.form['username']])
    except Exception, e:
        return fail(str(e))
    return success(account)


@app.route('/sbapp/1.0/activities')
def show_activities():
    try:
        activities = query_db('select * from activities')
    except Exception, e:
        return fail(str(e))
    return success(activities)


@app.route('/sbapp/1.0/add_activity', methods=['POST'])
def add_activity():
    db = get_db()
    f = request.form
    try:
        db.execute('insert into activities (title, content, cover_url) values (?, ?, ?)',\
            [f['title'], f['content'], f['cover_url']])
        db.commit()
    except Exception, e:
        return fail(str(e))
    return success("Add activity succeed")


@app.route('/sbapp/1.0/join_activity', methods=['POST'])
def join_activity():
    db = get_db()
    f = request.form
    try:
        if(query_db('select * from user_activity_join where uid=%s and aid=%s' % (f['uid'], f['aid']),\
            one=True) is not None):
            return fail("Already in activity")
        db.execute('insert into user_activity_join (uid, aid, time, operation, op_time) \
            values (?,?,?,?,?)', [f['uid'], f['aid'], time.time(), 1, time.time()])
        db.commit()
    except Exception, e:
        return fail(str(e))
    return success("Request sent")


@app.route('/sbapp/1.0/act_activity', methods=['POST'])
def act_activity():
    db = get_db()
    f = request.form
    try:
        db.execute('insert into user_activity_act (uid,aid,time,act,location,content) \
            values (?,?,?,?,?,?)', [f['uid'],f['aid'],time.time(),f['act'],f['location'],f['content']])
        db.commit()
    except Exception, e:
        return fail(str(e))
    return success("Act sent")


@app.route('/sbapp/1.0/acts', methods=['POST'])
def get_acts():
    f = request.form
    try:
        acts = query_db('select * from user_activity_act where aid=%s order by time asc' % (f['aid']))
    except Exception, e:
        return fail(str(e))
    return success(acts)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

