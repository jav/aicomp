import unittest

from account import Account

class AccountTestCase(unittest.TestCase):

    def setUp(self):
        Account.engine = create_engine('sqlite:///:memory:', echo=True)
        pass

    def tearDown(self):
        pass

    def testCreateAccount(self):
        acc = Account(user='user')
        self.assertRaise(TypeError, acc.save)
        acc = Account(user='user', passwd='passwd')
        self.assertRaise(TypeError, acc.save)
        acc = Account(user='user', passwd='passwd',email='email')
        acc.save()

        acc = Account.fetch(user='foo')
        assert acc is None
        acc = Account.fetch(user='user')
        assert acc.user == 'user'
        acc = Account.fetch(email='bar')
        assert acc is None
        acc = Account.fetch(email='email')
        assert acc.email == 'email'

    def testFetchAccount(self):
        # Hey, this test is redundant(!) with the previous, but I can't
        # decide what to test where, is this coupeled enough to
        # merge?

        acc = Account(user='user', passwd='passwd',email='email')
        acc.save()

        acc = Account.fetch(user='foo')
        assert acc is None
        acc = Account.fetch(user='user')
        assert acc.user == 'user'
        acc = Account.fetch(email='bar')
        assert acc is None
        acc = Account.fetch(email='email')
        assert acc.email == 'email'

    def testModifyAccount(self):
        # You'r allowed to change passwd & e-mail
        # But not your username!
        acc = Account(user='user', passwd='passwd',email='email')
        acc.save()
        acc = Account.fetch(user='user')
        assert acc.user == 'user'

        acc.user='newname'
        self.assertRaises(TypeError, acc.save)

        acc = Account.fetch(user='user')
        assert acc.user == 'user'
        assert acc.passwd == 'passwd'
        assert acc.email == 'email'
        acc.passwd = "newpass"
        acc.email = "newmail"
        acc.save()

        acc = None
        acc = Account.fetch(user='user')
        assert acc.user == 'user'
        assert acc.passwd == 'newpass'
        assert acc.email == 'newmail'


    def testDeleteAccount(self):
        acc = Account(user='user', passwd='passwd',email='email')
        acc.save()
        acc = Account.fetch(user='user')
        assert acc.user == 'user'

        acc.delete()
        acc = Account.fetch(user='user')
        assert acc is None

