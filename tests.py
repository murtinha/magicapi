from flask import json, jsonify, Flask
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
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTS
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

class MyTest(BaseTestCase):

# HEALTH-CHECK

	def test_health_check(self):

		response = self.client.get('/health-check')
		self.assertIn('It lives!!!', response.data)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# SHOW CARDS BY NAME

	def test_show_cards_by_name(self):

		response = self.client.get('/name/?name=Air+Elemental')

		return 'ok'           				                                  
		flat_response = response.data.replace('\n', '')
		flat_response = flat_response.replace(' ', '')
		r = json.dumps(dict(colors="[Blue]",
                            mana_cost="3UU",
                            name="Air Elemental",
                            subtypes="[Elemental]",
                            text="Flying",
                            types= "[Creature]"))
		r = r.replace(' ', '')
		self.assertEqual(r, flat_response)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# SHOW CARDS BY COLOR
	
	def test_show_cards_by_color(self):
		
		response = self.client.get('/colors/?colors=Green')
		
		flat_response = response.data.replace('\n', '')
		flat_response = flat_response.replace(' ', '')
		r = json.dumps(dict(names = ["Berserk", "Aspect of Wolf", "Birds of Paradise"]))
		r = r.replace(' ', '')
		self.assertEqual(r, flat_response)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
  
# SHOW CARD USERS

	def test_show_cards_users(self):
		
		user = Users('Eric','eric@murt.com')
		db.session.add(user)
		db.session.commit()
		card = Cards.query.filter_by(name = 'Canyon Slough').first()
		card.owner.append(user)
		response = self.client.get('/users/?name=Canyon Slough')

		flat_response = response.data.replace('\n', '')
		flat_response = flat_response.replace(' ', '')
		r = json.dumps(dict(usernames = ['Eric']))
		r = r.replace(' ', '')
		self.assertEqual(r, flat_response)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# SHOW CARDS BY TEXT
	
	def test_show_cards_by_text(self):

		response = self.client.get('/text/?text=flying')

		flat_response = response.data.replace('\n', '')
		flat_response = flat_response.replace(' ', '')
		r = json.dumps(dict(names = ["Air Elemental","Birds of Paradise","Companion of the Trials"]))
		r = r.replace(' ', '')
		self.assertEqual(r,flat_response)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# SHOW CARDS BY SUBTYPES
	
	def test_show_cards_by_subtypes(self):

		response = self.client.get('/subtypes/?subtypes=Aura')

		flat_response = response.data.replace('\n', '')
		flat_response = flat_response.replace(' ', '')
		r = json.dumps(dict(names = ["Animate Wall","Aspect of Wolf","Black Ward","Animate Dead","Animate Artifact"]))
		r = r.replace(' ', '')
		self.assertEqual(r,flat_response)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# SHOW CARDS BY SUBTYPES,COLOR,TEXT

	def test_show_cards_by_sub_color_text(self):

		response = self.client.get('/subtypes/colors/text/?subtypes=Bird&colors=White&text=flying')


		flat_response = response.data.replace('\n', '')
		flat_response = flat_response.replace(' ', '')
		r = json.dumps(dict(names = ["Companion of the Trials"]))
		r = r.replace(' ', '')
		self.assertEqual(r,flat_response)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# SHOW CARDS BY MANACOST
	
	def test_show_cards_by_manacost(self):

		response = self.client.get('/manacost/?manacost=3UU')


		flat_response = response.data.replace('\n', '')
		flat_response = flat_response.replace(' ', '')
		r = json.dumps(dict(names = ["Air Elemental"]))
		r = r.replace(' ', '')
		self.assertEqual(r ,flat_response)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# SHOW CARDS BY TYPE
	
	def test_show_cards_by_types(self):

		response = self.client.get('/types/?types=Creature,Artifact')


		flat_response = response.data.replace('\n', '')
		flat_response = flat_response.replace(' ', '')
		r = json.dumps(dict(names = ["Watchers of the Dead"]))
		r = r.replace(' ', '')
		self.assertEqual(r, flat_response)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# SHOW CARDS BY MANACOST AND COLOR

	def test_show_cards_by_manacost_colors(self):

		response = self.client.get('/manacost/colors/?manacost=W&colors=White')


		flat_response = response.data.replace('\n', '')
		flat_response = flat_response.replace(' ', '')
		r = json.dumps(dict(names = ["Animate Wall","Benalish Hero","Black Ward","Blaze of Glory"]))
		r = r.replace(' ', '')
		self.assertEqual(r,flat_response)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# ADDING USER

	def test_add_user(self):
		response = self.client.post('/adduser', data = json.dumps(dict(username = 'eric',
																	 email = 'eric@m.com')),
																	 content_type = 'application/json')


		user = Users.query.filter_by(username = 'eric').first()
		self.assertEqual('eric', user.username)
		self.assertEqual('eric@m.com', user.email)


if __name__ == '__main__':
    unittest.main()