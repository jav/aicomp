#!/usr/bin/env python

# Wouldn't it be nice if this was some more 'web-oriented' thing?
# But, now I just want stuff to work, so this is what I consider
# the shortest distance to getting shit done.

from flask import Flask, jsonify, render_template
import json

from account import Account

app = Flask(__name__)

#init

@app.route('/')
def front_page():
    return render_template('frontpage.html')

@app.route('/register', methods=['GET', 'POST'])
def login():
    # Create a new user
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    # login
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


if __name__ == "__main__":
    config = {}
    config = json.load(open('webfront.conf','r'))

    port = config.setdefault('port', 60000)
    app.run(debug=True, port=port)
