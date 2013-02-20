from random import randrange
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
# Right now, it pulls players randomly from the global list
# It would be nice if we used the priorityqueue to, some how, give priority to new players

import heapq

class QueueEmptyError(Exception):
    pass

class ChallengerElement(Base):
    __tablename__ = 'challengerelement'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    player_id = Column(Integer, ForeignKey("player.id"))
    relationship(Player, primaryjoin="player.id==challengerelement.player_id")

class ChallengeQueue(object):
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
        players = self._random_select_player_set(nr_players, db_session)
        print "players: %s" % (players,)
        return Match(state='unplaid', players=players)

    def __len__(self):
        return len(self.queue)

    def _update_players(self):
        pass

    def _random_select_player_set(self, count, session):
        query = session.query(Player)
        enabled_row_count =  int(query.filter_by(enabled=True).count()) # We are using the (broken) assumption that rowcount >= max(id)
                                                               # and we are not checking for unique owners.

        if count > enabled_row_count:
            raise IndexError("Not enough players available for a full match")

        row_count = int(query.count()) # We are using the (broken) assumption that rowcount >= max(id)
        print "count:%s, row_count:%s"%(count, row_count)
        result_set = set()
        while len(result_set) < count:
#            obj =  query.filter_by(id=int(row_count*random())).first()
            id = randrange(row_count+1)
            print "randrange(%s): %s"%(row_count, id)
            obj = query.filter_by(id=id).filter_by(enabled=True).first()
            print "result_set.add(%s), len(result_set): %s: result_set: %s "%(obj,len(result_set), result_set)
            if obj is None:
                continue # This dosen't feel right, but should work
            result_set.add(obj)

        print "_random_select_set(%s, %s) returns: %s"%(count, query, result_set)
        return list(result_set)

    def append(self, item, prio=0):
        #Set priority with prio, zero is highest
        heapq.heappush(self.queue, (prio, item))

    def pop(self):
        if not self.queue:
            raise QueueEmptyError
        else:
            return heapq.heappop(self.queue)[1]

    def __len__(self):
        return len(self.queue)
