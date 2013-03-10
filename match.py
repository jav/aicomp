from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import Enum, MetaData, ForeignKey, Table
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship

from database import Base, db_session
from player import Player

class PlayerResult(Base):
    __tablename__ = 'playerresult'

    result= Column(Integer)
    player_id = Column(Integer,ForeignKey('player.id'), primary_key=True)
    match_id = Column(Integer, ForeignKey('match.id'), primary_key=True)
    player = relationship(Player, primaryjoin="Player.id==PlayerResult.player_id")
    position = Column(Integer)

    def __init__(self, player, result=0):
        self.player=player
        self.result=result

    def serialize(self):
        return {
            "result": self.result,
            "player_id": self.player_id,
            "match_id": self.match_id,
            "player": self.player.serialize(),
            "position": self.position
            }

class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True)
    state = Column(String) #Enum('inprogress', 'sucessfull', 'unplayed', 'unsucessfull')
    playerresults = relationship(PlayerResult, primaryjoin="PlayerResult.match_id==Match.id", order_by="PlayerResult.position", collection_class=ordering_list('position')) # This _should_ be able to be an association_proxy(), but I can't figure it out right now.

    def __init__(self, **kwargs):
        print "Match.__init__(%s)" %(kwargs,)
        self.state = kwargs.get('state', 'unplayed')
        for p in kwargs.get('players',[]):
            pr = PlayerResult(p,0)
            self.playerresults.append(pr)
        #self.add_players(kwargs.get('players', []))

    def __repr__(self):
        return "<Match(state: '%s', playerresults: %s)>" % (self.state, self.playerresults)

    def serialize(self):
        '''Return object data in easily serializeable format'''
        return {
            'id'         : self.id,
            'playerresults': [x.serialize() for x in self.playerresults]
        }

