import unittest
from sqlalchemy import create_engine

from database import db_session, init_db, reset_db, engine as db_engine
from match import Match
from player import Player


class MatchTestCase(unittest.TestCase):
    def setUp(self):
        #Scope mix here is intentional, I don't like importing "engine" form database
        db_engine = create_engine('sqlite:///:memory:', echo=True)
        pass

    def tearDown(self):
        pass

    def testCreateTrivialMatch(self):
        init_db()
        match = Match()
        assert match.state == 'unplayed'
        db_session.add(match)
        db_session.commit()
        match_persist = db_session.query(Match).first()
        assert match_persist.state == 'unplayed'
        reset_db()

    def testSinglePlayerMatch(self):
        init_db()
        player_one = Player(owner=1, desc="I'm uniq", enabled=True)
        db_session.add(player_one)
        db_session.commit()
        match = Match(players=[player_one])
        assert match.state == 'unplayed'
        print "Match before commit: %s"%(match,)
        db_session.add(match)
        db_session.commit()
        match_persist = db_session.query(Match).first()
        print "Match re-read: %s"%(match_persist,)
        assert match_persist.playerresults[0].result == 0
        assert match_persist.playerresults[0].player.owner == 1
        assert match_persist.playerresults[0].player.desc == "I'm uniq"
        assert match_persist.playerresults[0].player.enabled == True
        reset_db()

    def testMultiPlayerMatch(self):
        init_db()
        player_one = Player(owner=1, desc="I'm uniq", enabled=True)
        db_session.add(player_one)
        db_session.commit()
        print "player_one.id:", player_one.id
        player_two = Player(owner=2, desc="I'm not", enabled=True)
        db_session.add(player_two)
        db_session.commit()
        print "player_two.id:", player_two.id
        match = Match(players=[player_one, player_two])
        db_session.add(match)
        assert match.state == 'unplayed'
        print "Match before commit: %s"%(match,)
        db_session.add(match)
        db_session.commit()
        match_persist = db_session.query(Match).first()
        print "Match re-read: %s"%(match_persist,)
        assert match_persist.playerresults[0].result == 0
        assert match_persist.playerresults[0].player.owner == 1
        assert match_persist.playerresults[0].player.desc == "I'm uniq"
        assert match_persist.playerresults[0].player.enabled == True
        assert match_persist.playerresults[1].result == 0
        assert match_persist.playerresults[1].player.owner == 2
        assert match_persist.playerresults[1].player.desc == "I'm not"
        assert match_persist.playerresults[1].player.enabled == True
        reset_db()

    def testSinglePlayerMatchSerialize(self):
        init_db()
        player_one = Player(owner=1, desc="I'm uniq", enabled=True)
        db_session.add(player_one)
        db_session.commit()
        print "player_one.id:", player_one.id
        player_two = Player(owner=2, desc="I'm not", enabled=True)
        db_session.add(player_two)
        db_session.commit()
        print "player_two.id:", player_two.id
        match = Match(players=[player_one, player_two])
        db_session.add(match)
        assert match.state == 'unplayed'
        print "Match before commit: %s"%(match,)
        db_session.add(match)
        db_session.commit()
        match_persist = db_session.query(Match).first()
        print match_persist

        serialized_match = match_persist.serialize()
        assert len(seralized_match['playerresults']) == 2

        reset_db()
