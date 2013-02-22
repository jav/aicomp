from random import random
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import Enum, MetaData, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base, db_session
from match import Match
from player import Player

# TODO: This should also keep rankings
# And have some sensible way of picking matches so that you can't, e.g.
# flood the game with your own players, where all but one have one exact weakness
# that the last one always exploits.

class QueueEmptyError(Exception):
    pass

class ChallengerElement(Base):
    __tablename__ = 'challengerelement'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    player_id = Column(Integer, ForeignKey("player.id"))
    relationship(Player, primaryjoin="player.id==challengerelement.player_id")

    def __init__(self):
        pass

class ChallengeQueue(Base):
    __tablename__ = 'challengequeue'

    id = Column(Integer, primary_key=True) # There should be a better primary key for this!
    #challengers = relationship(ChallengerElement)

    def __init__(self):
        self._update_players()
        pass

    def get_match(self, nr_players):
        players = self._random_select_set(nr_players, db_session.query(Player))
        print "players: %s" % (players,)
        return Match(state='unplaid', players=players)

    def __len__(self):
        return len(self.queue)


    def _update_players(self):
        pass

    def _random_select_set(self, count, query):
        row_count = int(query.count())

        result_set = set()
        while len(result_set) < count:
            obj =  query.offset(int(row_count*random())).first()
            print "result_set.add(%s), len(result_set): %s"%(obj,len(result_set))
            result_set.add(obj)

        print "_random_select_set(%s, %s) returns: %s"%(count, query, result_set)
        return list(result_set)
