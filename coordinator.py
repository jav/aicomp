#!/usr/bin/env python

from flask import Flask, jsonify

from database import init_db, db_session
from challenge_queue import ChallengeQueue
from match import Match
from player import Player

app = Flask(__name__)

@app.route('/match/get/<int:nr_p>')
def get_challenge_from_queue(nr_p):
    ''' The game-master/worker polls for a match (with n numer of players)
    reply:
    if there are enough players:
    { "match_id": <int:id>, "p": [ (<int:player_id, <string:files_URI>), ... ] }
    if there are not enough players:
    { "match_id": -1, "error": <str:errmsg>
    '''
    challenge_queue = app.config['CHALLENGE_QUEUE']
    players = []
    match = challenge_queue.get_match(2)
    db_session.add(match)
    db_session.commit()

    return jsonify(match.serialize())

@app.route('/match/list')
def matches_list():
    matches = []
    for match in db_session.query(Match).all():
        matches.append(match.serialize())
        #print matches
    return jsonify([x.serialize() for x in db_session.query(Match).all() ] )

@app.route('/player/<int:player_id>/files')
def get_player_files(player_id):
    pass

if __name__ == '__main__':
    init_db()
    app.config['CHALLENGE_QUEUE'] = ChallengeQueue()
    app.run(debug=True)
