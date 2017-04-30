
from app import db
from flask import json


# RELATIONAL TABLE

decks = db.Table('decks',
		db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
		db.Column('id', db.String, db.ForeignKey('cards.id'))
	)

# TABLE FOR CARDS

class Cards(db.Model):
	__tablename__ = 'cards'

	id = db.Column(db.String, primary_key = True)
	name = db.Column(db.String, unique = True)
	manaCost = db.Column(db.String) # "2WUB"
	colors = db.Column(db.String) # "["White", "Blue", "Black"]"
	types = db.Column(db.String) # "["Artifact","Creature"]"
	rarity = db.Column(db.String) 
	text = db.Column(db.String)
	artist = db.Column(db.String)
	owners = db.relationship('Users', secondary = decks, backref = db.backref('mycards', lazy = 'dynamic'))

	def __init__(self,id,name, manaCost, colors, types, rarity, text, artist):
		
		self.id = id
		self.name = name
		self.manaCost = manaCost
		self.colors = colors
		self.types = types
		self.rarity = rarity	
		self.text = text
		self.artist = artist

	def __repr__(self):

		return json.dumps(dict(id = self.id,
							   name = self.name,
							   manaCost = self.manaCost,
							   colors = self.colors,
							   types = self.types,
							   rarity = self.rarity,
							   text = self.text,
							   artist = self.artist))

# TABLE FOR USERS

class Users(db.Model):
	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String, unique = True)
	email = db.Column(db.String, unique = True)
	user_cards = db.relationship('Cards', secondary = decks, backref = db.backref('owner', lazy = 'dynamic'))
	# cards_id = db.Column(db.String, db.ForeignKey('cards.id'))
	# clan = db.Column(db.Integer, db.ForeignKey('clans.id'))

	def __init__(self,username,email):

		self.username = username
		self.email = email
		# self.cards = cards_id
		# self.clan = clan











		

# TABLE FOR CLANS

# class Clans(db.Model):
# 	__tablename__ = 'clans'

# 	id = db.Column(db.String, primary_key = True)
# 	name = db.Column(db.String, unique = True)
# 	usernames = db.relationship('Users', backref = 'clans', lazy = 'dynamic')  

# 	def __init__(self,name,usernames):

# 		self.name = name
# 		self.usernames = usernames


# ONE CARD CAN HAVE MANY USERS
# ONE USER CAN HAVE MANY CARDS BUT ONE CLAN
# ONE CLAN CAN HAVE MANY USERS