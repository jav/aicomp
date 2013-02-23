#!/usr/bin/env python

# Wouldn't it be nice if this was some more 'web-oriented' thing?
# But, now I just want stuff to work, so this is what I consider
# the shortest distance to getting shit done.

from flask import Flask, jsonify, render_template, session
from flask import request, redirect, url_for
import json
import os
import shutil
import tempfile
from werkzeug import secure_filename

from account import Account
from database import init_db, db_session
from player import Player

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
            account = create_account(user, password, email)
            session['logged_in'] = True
            session['user'] = db_session.query(Account).filter_by(user=user).first()

            return redirect(url_for('front_page', errors=error))
    return render_template('account_register.html', errors=error)    # Create a new user

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
    return render_template('player_list.html', players=players)

@app.route('/player/add', methods=['GET', 'POST'])
def player_add():
    if not is_logged_in():
        return render_template('frontpage.html', errors="Login required.")

    error = []

    # upload a player
    if request.method == 'POST':
        if 'player_archive' not in request.files:
            error.append("Failed to upload archive.")
        else:
            f = request.files['player_archive']
            filename = secure_filename(f.filename)
            print "filename:", filename
            (_ ,ext) = os.path.splitext(filename)
            ext = ext.strip('.')
            if ext not in app.config['UPLOAD_FILE_EXT']:
                error.append("Extension %s not allowed."%ext)
            else:
                tmp_file = os.path.join(tempfile.mkdtemp(), filename)
                f.save(tmp_file)

                acc_id = session['user'].id
                player = create_player(owner=acc_id, desc=request.form['desc'])
                pl_id = player.id
                dest_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(acc_id), str(pl_id)
)
                try:
                    os.makedirs(dest_dir, 0770)
                except OSError:
                    pass # Because OSError == dir already exists

                dest_file = os.path.join(dest_dir, filename)
                shutil.move(tmp_file, dest_file)
                player.files = dest_file
                return redirect(url_for('player_list', filename=filename))

            if err:
                error.append(err)
            else:
                session['logged_in'] = True
                session['user'] = db_session.query(Account).filter_by(user=user).first()

            return redirect(url_for('player_list', errors=error))

    return redirect(url_for('player_list', errors=error)) # Redirect, because you shouldn't get here through GET

@app.route('/player/edit/<int:acc_id>/<int:pl_id>', methods=['GET', 'POST'])
def player_edit(acc_id, pl_id):
    # NO! Not OK!
    # Modifying an existing and ranked player is uncool
    # We should be able to learn from the submissions, and
    # this would kill history.
    # nope nope nope nope. Uncool!
    # Well, enable/disable would be nice.
    # And maybe a comment (or log field)

    if not is_logged_in():
        return render_template('frontpage.html', errors="Login required.")
    error = []
    player = db_session.query(Player).filter_by(owner=acc_id).filter_by(id=pl_id).first()
    if not player:
        return "NO SUCH PLAYER!"
    if session['user'].id != player.owner:
        return "NOT YOUR PLAYER! Your id is %d, player owner is: %d" % (session['user'].id, player.owner)

    if request.method == 'POST':
        return render_template('player_edit.html', player=player, errors=error)

    return render_template('player_edit.html', player=player, errors=error)

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
        raise TypeError("Username already exists.")
    if db_session.query(Account).filter_by(email=email).first() is not None:
        raise TypeError("E-mail already registered.")

    acc = Account(user=user, passwd=passwd, email=email)
    db_session.add(acc)
    db_session.commit()
    return acc

def create_player(**kwargs):
    for k in ['owner', 'desc']:
        if k not in kwargs:
            raise TypeError("Either owner or desc not defined")

    # TODO: player should have a foregin key to its owner
    # TODO: Doublecheck that the owner exists

    player = Player(owner=kwargs['owner'], desc=kwargs['desc'])
    db_session.add(player)
    db_session.commit()
    return player

def is_logged_in():
    if not session['logged_in']:
        return False
    return True

if __name__ == "__main__":
    config = json.load(open('webfront.conf','r'))

    for k,v in config.iteritems():
        app.config[k] = v

    print "app.config", app.config

    init_db()

    app.secret_key = 'UNKNOWN_STRING' #Yes, a popular reference. Let's later fix this (famous last words)
    app.run(port=app.config['PORT'])
