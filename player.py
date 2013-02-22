from sqlalchemy import Column, Integer, String, Boolean, MetaData

from database import Base, db_session

class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    owner = Column(Integer)
    desc = Column(String)
    files = Column(String)
    enabled = Column(Boolean)

    def __init__(self, **kwargs):
        if 'owner' not in kwargs:
            raise TypeError("A Player must have an owner.")

        self.owner = kwargs['owner']
        self.desc = kwargs.get('desc', '')
        self.files = kwargs.get('files', None)

    def __repr__(self):
        return "<Player(owner:'%s', desc:'%s', files: %s)>" % (self.owner, self.desc, self.files)

    def add_files_uri(self, files):
        self.files = files

    def get_files_uri(self):
        return self.files

    def serialize(self):
        '''Return object data in easily serializeable format'''
        return {
            'id'      : self.id,
            'owner'   : self.owner,
            'desc'    : self.desc,
            'files'   : self.files,
            'enabled' : self.enabled
        }
