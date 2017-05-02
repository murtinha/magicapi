
from app import db
from flask import json


# RELATIONAL TABLE

decks = db.Table('decks',
		db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
		db.Column('id', db.Integer, db.ForeignKey('cards.id'))
	)

# TABLE FOR CARDS

class Cards(db.Model):
	__tablename__ = 'cards'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, unique = True)
	manaCost = db.Column(db.String) # "2WUB"
	colors = db.Column(db.String) # "["White", "Blue", "Black"]"
	types = db.Column(db.String) # "["Artifact","Creature"]"
	text = db.Column(db.String)
	subtypes = db.Column(db.String)
	owners = db.relationship('Users', secondary = decks, backref = db.backref('mycards', lazy = 'dynamic'))

	def __init__(self,name, manaCost, colors, types, subtypes,text ):
		
		self.name = name
		self.manaCost = manaCost
		self.colors = colors
		self.types = types
		self.subtypes = subtypes
		self.text = text

	def __repr__(self):

		return json.dumps(dict(id = self.id,
							   name = self.name,
							   manaCost = self.manaCost,
							   colors = self.colors,
							   types = self.types,
							   subtypes = self.subtypes,
							   text = self.text))

# TABLE FOR USERS

class Users(db.Model):
	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String, unique = True)
	email = db.Column(db.String, unique = True)
	user_cards = db.relationship('Cards', secondary = decks, backref = db.backref('owner', lazy = 'dynamic'))
	clan = db.relationship('Clans', backref = db.backref('adepts'),uselist =  False)

	def __init__(self,username,email):

		self.username = username
		self.email = email

	def __repr__(self):

		return json.dumps(dict(username = self.username,
							   email = self.email))



# TABLE FOR CLANS

class Clans(db.Model):
	__tablename__ = 'clans'

 	id = db.Column(db.String, primary_key = True)
 	clan_name = db.Column(db.String, unique = True)
 	adepts_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
 	def __init__(self,clan_name):

 		self.clan_name = clan_name


# ONE CARD CAN HAVE MANY USERS
# ONE USER CAN HAVE MANY CARDS BUT ONE CLAN
# ONE CLAN CAN HAVE MANY USERS