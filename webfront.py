#!/usr/bin/env python

# Wouldn't it be nice if this was some more 'web-oriented' thing?
# But, now I just want stuff to work, so this is what I consider
# the shortest distance to getting shit done.

from flask import Flask, jsonify, render_template, session
from flask import request, redirect, url_for
import json
from werkzeug import secure_filename

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
            err = create_account(user, password, email)
            if err:
                error.append(err)
            else:
                session['logged_in'] = True
                session['user'] = db_session.query(Account).filter_by(user=user).first()

            return redirect(url_for('front_page', error=error))
    return render_template('register.html', error=error)    # Create a new user

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = []
    if request.method == 'POST':
        if 'user' in request.form and len(request.form['user']) > 0 and  'password' in request.form:
            acc = db_session.query(Account).filter_by(user=request.form['user']).first()

            if not acc:
                error.append("User does not exist.")
                return "ERROR - Wrong user or passwd.."

            if not acc.test_passwd(request.form['password']):
                return "ERROR - Wrong user or passwd."

            session['logged_in'] = True
            session['user'] = acc
            players = acc.get_players()
            return redirect(url_for('player_list', players=players))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('user', None)
    return render_template('frontpage.html')
    pass

@app.route('/account/modify', methods=['GET', 'POST'])
def modify_account():
    return "NOT YET IMPLEMENTED"

@app.route('/account/delete', methods=['GET', 'POST'])
def delete_account():
    # This should not allow some other account to take whichever
    # we are key:ing accounts on, be it id or name.
    # Let's tag them as deleted and ignore them.
    return "NOT YET IMPLEMENTED"

@app.route('/player/list')
def player_list():
    if not session['logged_in']:
        return "REQUIRES LOGIN"
    acc = session['user']
    players=acc.get_players()
    return render_template('players_for_account.html', players=players)

@app.route('/player/add', methods=['GET', 'POST'])
def player_add():
    error = []

    # upload a player
    if request.method == 'POST':
        if 'player_archive' not in request:
            error.append("Failed to upload archive.")
        else:
            f = request.files['player_archive']
            filename = secure_filename(f.filename)
            (_ ,ext) = os.path.splitext(filename)
            ext = ext.strip('.')
            if ext not in ['tar', 'zip', 'gz']:
                error.append("Extension %s not allowed."%ext)
            else:
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
            

            err = create_player(desc, )
            if err:
                error.append(err)
            else:
                session['logged_in'] = True
                session['user'] = db_session.query(Account).filter_by(user=user).first()

            return redirect(url_for('front_page', error=error))

    return "NOT YET IMPLEMENTED"

@app.route('/player/modify', methods=['GET', 'POST'])
def player_modify():
    # NO! Not OK!
    # Modifying an existing and ranked player is uncool
    # We should be able to learn from the submissions, and
    # this would kill history.
    # nope nope nope nope. Uncool!
    return "NOT YET IMPLEMENTED"

@app.route('/player/delete', methods=['GET', 'POST'])
def player_delete():
    # Removing a player entierly is ok.
    # Keep in mind to not reuse key-id (id, name, whatever)
    return "NOT YET IMPLEMENTED"

# Wrong verison of Flask?
#@app.teardown_request
#def shutdown_session(exception=None):
#    '''kill db sessions at the end of each request'''
#    db_session.remove()

def get_accounts(start=0, end=-1):
    #start, end not yet implemented
    return db_session.query(Account).all()

def create_account(user, passwd, email):
    if db_session.query(Account).filter_by(user=user).first() is not None:
        return False
    if db_session.query(Account).filter_by(email=email).first() is not None:
        return False

    acc = Account(user=user, passwd=passwd, email=email)
    db_session.add(acc)
    db_session.commit()
    return acc

class DictToConfObject(object):
    def __init__(self, d):
        for k,v in d.iteritems():
            setattr(self, k.upper(), v)

if __name__ == "__main__":
    config = {}
    config = json.load(open('webfront.conf','r'))

    for k,v in config.iteritems():
        app.config[k] = v

    print "app.config", app.config

    init_db()


    app.secret_key = 'UNKNOWN_STRING' #Yes, a popular reference. Let's later fix this (famous last words)
    app.run(port=app.config['PORT'])
