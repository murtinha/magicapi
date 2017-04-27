
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
