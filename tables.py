
from app import db
from flask import json


# RELATIONAL TABLES

card_decks_relationship = db.Table('decks_relationship',
		db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
		db.Column('card_id', db.Integer, db.ForeignKey('cards.card_id'))
	)

card_colors_relationship = db.Table('colors_relationship',
		db.Column('id', db.Integer, db.ForeignKey('colors.id')),
		db.Column('card_id', db.Integer, db.ForeignKey('cards.card_id'))
	)

card_types_relationship = db.Table('types_relationship',
		db.Column('id', db.Integer, db.ForeignKey('types.id')),
		db.Column('card_id', db.Integer, db.ForeignKey('cards.card_id'))
	)

card_subtypes_relationship = db.Table('subtypes_relationship',
		db.Column('id', db.Integer, db.ForeignKey('subtypes.id')),
		db.Column('card_id', db.Integer, db.ForeignKey('cards.card_id'))
	)


# TABLES FOR CARDS


class Colors(db.Model):
	__tablename__ = 'colors'

	id = db.Column(db.Integer, primary_key = True)
	color = db.Column(db.String, unique = True)
	card_color = db.relationship('Cards', secondary = card_colors_relationship, backref = db.backref('colorsref'))

	def __init__(self, color):

		self.color = color

	def __repr__(self):

		return self.color

class Types(db.Model):
	__tablename__ = 'types'

	id = db.Column(db.Integer, primary_key = True)
	types = db.Column(db.String, unique = True)
	card_types = db.relationship('Cards', secondary = card_types_relationship, backref = db.backref('typesref'))

	def __init__(self, types):

		self.types = types

	def __repr__(self):

		return self.types

class Subtypes(db.Model):
	__tablename__ = 'subtypes'

	id = db.Column(db.Integer, primary_key = True)
	subtype = db.Column(db.String, unique = True)
	card_subtype = db.relationship('Cards', secondary = card_subtypes_relationship, backref = db.backref('subtypesref')) 

	def __init__(self, subtype):

		self.subtype = subtype

	def __repr__(self):

		return self.subtype

class Cards(db.Model):
	__tablename__ = 'cards'

	card_id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, unique = True)
	mana_cost = db.Column(db.String)
	colors = db.relationship('Colors', secondary = card_colors_relationship, backref = db.backref('colorcards', lazy = 'dynamic'))
	types = db.relationship('Types', secondary = card_types_relationship, backref = db.backref('typecards', lazy = 'dynamic'))
	subtypes = db.relationship('Subtypes', secondary = card_subtypes_relationship, backref = db.backref('subtypescards', lazy = 'dynamic'))
	text = db.Column(db.String)
	owners = db.relationship('Users', secondary = card_decks_relationship, backref = db.backref('mycards', lazy = 'dynamic'))

	def __init__(self,name, mana_cost,text):
		
		self.name = name
		self.mana_cost = mana_cost
		self.text = text

	def __repr__(self):

		return json.dumps(dict(card_id = self.card_id,
							   name = self.name,
							   mana_cost = self.mana_cost,
							   text = self.text))

# TABLE FOR USERS

class Users(db.Model):
	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String, unique = True)
	email = db.Column(db.String, unique = True)
	user_cards = db.relationship('Cards', secondary = card_decks_relationship, backref = db.backref('owner', lazy = 'dynamic'))
	clan_ref = db.relationship('Clans', backref = db.backref('clanusers', lazy = 'dynamic'))
	my_clan = db.Column(db.Integer, db.ForeignKey('clans.clan_id'))

	def __init__(self,username,email):
		self.username = username
		self.email = email

	def __repr__(self):
		return json.dumps(dict(username = self.username,
							   email = self.email))



# TABLE FOR CLANS

class Clans(db.Model):
	__tablename__ = 'clans'

 	clan_id = db.Column(db.Integer, primary_key = True)
 	clan_name = db.Column(db.String, unique = True)
	

 	def __init__(self,clan_name):
 		self.clan_name = clan_name

 	def __repr__(self):
 		return json.dumps(dict(clan = self.clan_name))


# ONE CARD CAN HAVE MANY USERS
# ONE USER CAN HAVE MANY CARDS BUT ONE CLAN
# ONE CLAN CAN HAVE MANY USERS