from sqlalchemy import Column, Integer, String, Boolean, MetaData

from database import Base, db_session

class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    owner = Column(Integer)
    desc = Column(String)
    files = Column(String)
    enabled = Column(Boolean)
    games_played = Column(Integer)
    score = Column(Integer)

    def __init__(self, **kwargs):
        if 'owner' not in kwargs:
            raise TypeError("A Player must have an owner.")

        self.id = None
        self.owner = kwargs['owner']
        self.desc = kwargs.get('desc', '')
        self.files = kwargs.get('files', None)
        self.enabled = True
        self.games_played = 0
        self.score = 0

    def __repr__(self):
        return "<Player(id:%s owner:%d, desc:'%s', files: %s, games_played: %d, score: %d)>" % (self.id, self.owner, self.desc, self.files, self.games_played, self.score)

    def serialize(self):
        '''Return object data in easily serializeable format'''
        return {
            'id'      : self.id,
            'owner'   : self.owner,
            'desc'    : self.desc,
            'files'   : self.files,
            'enabled' : self.enabled,
            'games_played': self.games_played,
            'score'   : self.score
        }
