from flask import jsonify
import unittest

import webfront

class WebFrontTestCase(unittest.TestCase):

    def setUp(self):
        self.app = webfront.app.test_client()

    def tearDown(self):
        pass

#    def test_contestants(self):
#        rv = self.app.get('/')
#        print rv.data
#        assert len(rv.data) == 0
