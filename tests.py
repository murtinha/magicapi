from flask import json, Flask
from app import app,db
from tables import Cards, Users, Clans, Colors, Types, Subtypes
import unittest
from flask_testing import TestCase
from populatetest import populate_tests, map_tests

class BaseTestCase(TestCase):


    def create_app(self):     
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):        
        db.create_all()
        populate_tests()
        map_tests()

    def tearDown(self):        
        db.session.remove()
        db.drop_all()
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# TESTS
# --------------------------------------------------------------------------------------

class MyTest(BaseTestCase):

# HEALTH-CHECK

	def test_health_check(self):

		response = self.client.get('/health-check')
		self.assertIn('It lives!!!', response.data)
# --------------------------------------------------------------------------------------

# SHOW CARDS BY NAME

	def test_show_cards_by_name(self):

		response = self.client.get('/name',data = json.dumps(dict(name='Air Elemental')),
                                                                  content_type='application/json')
		print response.data




if __name__ == '__main__':
    unittest.main()