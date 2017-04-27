
from app import db
from flask import json


# TABLE FOR CARDS

class Cards(db.Model):

	id = db.Column(db.String, primary_key = True)
	name = db.Column(db.String, unique = True)
	manaCost = db.Column(db.String) # "{2}{W}{U}{B}"
	colors = db.Column(db.String) # "["White", "Blue", "Black"]"
	types = db.Column(db.String) # ["Artifact","Creature"]
	rarity = db.Column(db.String) 
	text = db.Column(db.String)
	artist = db.Column(db.String)

	def __init__(self, name, manaCost, colors, types, rarity, text, artist):
		
		self.name = name
		self.manaCost = manaCost
		self.colors = colors
		self.types = types
		self.rarity = rarity
		self.text = text
		self.artist = artist

# TABLE FOR USERS

class Users(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String, unique = True)
	email = db.Column(db.String, unique = True)
	cards = db.relationship('Cards', backref = 'users', lazy = 'dynamic')
	clan = db.Column(db.Integer, db.ForeignKey('clan.id'))

	def __init_(self,username,email,cards,clan):

		self.username = username
		self.email = email
		self.cards = cards
		self.clan = clan

# TABLE FOR CLANS

class Clans(db.Model):
	id = db.Column(db.String, primary_key = True)
	name = db.Column(db.String, unique = True)
	usernames = db.relationship('Users', backref = 'clans', lazy = 'dynamic')  

	def __init__(self,name,usernames):

		self.name = name
		self.usernames = usernames


# ONE USER HAS MANY CARDS BUT ONE CLAN
# ONE CLAN HAS MANY USERS