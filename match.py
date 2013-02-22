from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import Enum, MetaData, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base, db_session
from player import Player

player_to_match_relation = Table('player_to_match_relation', Base.metadata,
    Column('player_id', Integer, ForeignKey('player.id')),
    Column('match_id', Integer, ForeignKey('match.id'))
)

player_to_matchresultelement_relation = Table('player_to_matchresultelement_relation', Base.metadata,
    Column('player_id', Integer, ForeignKey('player.id')),
    Column('matchresultelement_id', Integer, ForeignKey('matchresultelement.id'))
)


class MatchResultElement(Base):
    __tablename__ = 'matchresultelement'

    id = Column(Integer, primary_key=True) # There should be a better primary key for this!
    match_id = Column(Integer, ForeignKey("match.id"), primary_key=True)
    player_id = Column(Integer, ForeignKey("player.id"))
    relationship(Player, secondary=player_to_matchresultelement_relation)
    score = Column(Integer)


class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True)
    players = relationship(Player, secondary=player_to_match_relation)
    state = Column(String) #Enum('inprogress', 'sucessfull', 'unplaid', 'unsucessfull')
    result = relationship(MatchResultElement, primaryjoin="Match.id == MatchResultElement.match_id")

    def __init__(self, **kwargs):
        print "Match.__init__(%s)" %(kwargs,)
        self.state = kwargs.get('state', 'unplaid')
        print "Match.__init__(): self.players = %s" % (kwargs.get('players', []))
        self.players = kwargs.get('players', [])
        print "Match.__init__(): self.result = []"
        self.result = []
        print "Match.__init__() returns: self"

    def __repr__(self):
        return "<Match(state: '%s', players: %s)>" % (self.state, self.players)

    def serialize(self):
       '''Return object data in easily serializeable format'''
       return {
           'id'         : self.id,
           'players': [x.serialize() for x in self.players],
       }

