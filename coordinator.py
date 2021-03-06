#!/usr/bin/env python

from flask import Flask, jsonify, session
from flask import request

import json

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
    try:
        challenge_queue = app.config['CHALLENGE_QUEUE']
        players = []
        match = challenge_queue.get_match(2)
        db_session.add(match)
        db_session.commit()
        print "match.serialize()", match.serialize()
        return jsonify(match.serialize())

    except Exception as ex:
        print "get_challenge_from_queue(): Exception: %s"%(ex,)
        return jsonify([])


@app.route('/match/list/json')
def match_list_json():
    matches = []
    try:
        for match in db_session.query(Match).all():
            matches.append(match.serialize())
            #print matches

        return jsonify([x.serialize() for x in db_session.query(Match).all() ] )
    except Exception:
        return jsonify([])

@app.route('/match/report/<int:match_id>', methods=['POST'])
def match_report(match_id):
    print "match_report(%d): request.method: %s"%(match_id, request.method)
    match_post = request.form
    for k,v in match_post.iteritems():
        print "k: %s, v: %s"%(k,v)
#    print "match_post: %s"%(match_post,)
    print "assert %d == %d" %(int(match_post['id']), match_id)
    assert int(match_post['id']) == match_id
    print "assert OK!"
    match = db_session.query(Match).filter_by(id = match_id).first()
    print "Match loaded: %s"%(match)
    print "Match state: %s"%(match_post['state'],)
    match.state = match_post['state']
    print "match_post", match_post
    db_session.add(match)
    db_session.commit()

    for playerresult in match.playerresults:
        p = db_session.query(Player).filter_by(id=playerresult.player_id).first()
        p.games_played += 1
        db_session.add(p)
        print "Player p:%s played a game, played games +=1"%(p,)
    db_session.commit() #this might break for a 0-player game, but is that even possible?
    return "MATCH REPORT RECEIVED!"


@app.route('/player/<int:player_id>/files')
def get_player_files(player_id):
    pass

if __name__ == '__main__':
    config = json.load(open('coordinator.conf','r'))
    for k,v in config.iteritems():
        app.config[k] = v
    print "app.config", app.config
    init_db()
    app.config['CHALLENGE_QUEUE'] = ChallengeQueue()
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])
