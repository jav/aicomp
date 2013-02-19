#!/usr/bin/env python

# Wouldn't it be nice if this was some more 'web-oriented' thing?
# But, now I just want stuff to work, so this is what I consider
# the shortest distance to getting shit done.

from flask import Flask, jsonify, render_template, session
from flask import request, redirect, url_for
import json

from account import Account
from database import init_db, db_session

app = Flask(__name__)

#init

@app.route('/')
def front_page():
    members=get_accounts()
    return render_template('frontpage.html', members=members)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = []

    if request.method == 'POST':
        print "request is POST"
        if len(request.form['user']) < 3:
            error.append('Invalid username')
        elif len(request.form['password1']) < 3:
            error.append('Invalid password')
        elif request.form['password1'] != request.form['password2']:
            error.append('Passwords do not match')
        elif len(request.form['email']) < 3:
            error.append('Invalid email (too short!)')
        else:
            (user, password, email) = [request.form[x] for x in ['user', 'password1', 'email']]
            print (user, password, email)
            create_account(user, password, email)
            session['logged_in'] = True
            return redirect(url_for('front_page'))
    return render_template('register.html', error=error)    # Create a new user

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/logout')
def logout():
    pass

@app.route('/account/modify', methods=['GET', 'POST'])
def modify_account():
    pass

@app.route('/account/delete', methods=['GET', 'POST'])
def delete_account():
    # This should not allow some other account to take whichever
    # we are key:ing accounts on, be it id or name.
    # Let's tag them as deleted and ignore them.
    pass


@app.route('/player/add', methods=['GET', 'POST'])
def player_add():
    # upload a player
    pass

@app.route('/player/modify', methods=['GET', 'POST'])
def player_modify():
    # NO! Not OK!
    # Modifying an existing and ranked player is uncool
    # We should be able to learn from the submissions, and
    # this would kill history.
    # nope nope nope nope. Uncool!
    pass

@app.route('/player/delete', methods=['GET', 'POST'])
def player_delete():
    # Removing a player entierly is ok.
    # Keep in mind to not reuse key-id (id, name, whatever)
    pass

# Wrong verison of Flask?
#@app.teardown_request
#def shutdown_session(exception=None):
#    '''kill db sessions at the end of each request'''
#    db_session.remove()

def get_accounts(start=0, end=-1):
    #start, end not yet implemented
    return db_session.query(Account).all()

def create_account(user, passwd, email):
    acc = Account(user=user, passwd=passwd, email=email)
    db_session.add(acc)
    db_session.commit()

if __name__ == "__main__":
    config = {}
    config = json.load(open('webfront.conf','r'))

    init_db()

    port = config.setdefault('port', 60000)
    app.secret_key = 'UNKNOWN_STRING' #Yes, a popular reference. Let's later fix this (famous last words)
    app.run(debug=True, port=port)
