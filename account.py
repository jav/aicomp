import hashlib
import random
from sqlalchemy import Column, Integer, String
from types import NoneType

from database import Base, db_session
from player import Player

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    user = Column(String)
    passwd = Column(String)
    salt = Column(String)
    email = Column(String)

    def __init__(self, **kwargs):
        if 'user' not in kwargs:
            raise TypeError("An Account must have a username.")
        if 'passwd' not in kwargs:
            raise TypeError("An Account must have a password.")
        if 'email' not in kwargs:
            raise TypeError("An Account must have an email.")

        self.user = kwargs['user']
        self.email = kwargs['email']
        (self.salt, self.passwd) = self.gen_passwd(kwargs['passwd'])

    def __repr__(self):
        return "<Account(user:'%s', email:'%s')>" % (self.user, self.email)

    def gen_passwd(self, passwd_str):
        m = hashlib.sha1()
        alphabet = map(chr, range(97, 123)) + map(chr, range(65, 91))
        self.salt = ''.join(random.choice(alphabet) for i in range(128))
        m.update(self.salt+passwd_str)
        return (self.salt, m.hexdigest())

    def test_passwd(self, passwd_str):
        m = hashlib.sha1()
        m.update(self.salt+passwd_str)
        return self.passwd == m.hexdigest()

    def get_players(self, db=None):
        if db is None:
            db = db_session
        return db.query(Player).filter_by(owner=self.id).all()
