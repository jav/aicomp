from sqlalchemy import Column, Integer, String, MetaData

from database import Base, db_session

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    owner = Column(String)
    desc = Column(String)
    files = Column(String)

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

