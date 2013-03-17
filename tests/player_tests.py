from sqlalchemy import create_engine
import tempfile
import unittest


from database import db_session, init_db, reset_db, engine as db_engine
from player import Player

class PlayerTestCase(unittest.TestCase):

    def setUp(self):
        (db_f, db_file) = tempfile.mkstemp()
        db_engine = create_engine('sqlite://%s'%db_file, echo=True)
        pass

    def tearDown(self):
        pass

    def testPersistPlayer(self):
        init_db()
        #You must specify an onwer to be allowed to create a player
        player = Player(owner=1, desc="My description.", files="null_tmpfile")
        self.assertTrue(player.desc == "My description.")
        print "player, pre add()", player
        db_session.add(player)
        print "player, pre commit()", player
        db_session.commit()
        print "player, post commit()", player
        pid = player.id
        player_persist = db_session.query(Player).first()
        print "pid =", pid
        print "player_presist", player_persist
        self.assertTrue(player_persist.id == pid)
        self.assertTrue(player_persist.desc == "My description.")
        reset_db()


