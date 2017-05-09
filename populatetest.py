from flask import json
from app import app,db
from tables import *
import re

# GETTING CARDS FROM JSON

with open('demo.json') as json_data:
		json_test_cards = json.load(json_data, strict = False)


# GETTING ALL SINGLE TYPES AND SUBTYPES

types = map(lambda card: card.get('types',''),json_test_cards.values())
subtypes = map(lambda card: card.get('subtypes',''),json_test_cards.values())
types_flatten = ()
subtypes_flatten = ()

for type in types:
	types_flatten += tuple(type)
types_flatten = list(set(types_flatten))

for subtype in subtypes:
	subtypes_flatten += tuple(subtype)
subtypes_flatten = list(set(subtypes_flatten))





def populate_tests():

	# POPULATING CARDS

	for card in json_test_cards.values():
		card_name = card.get('name', '')
		card_mana_cost = re.sub("\W", "",card.get('manaCost', ''))
		card_mana_cost_split = []
		for word in card_mana_cost:
			card_mana_cost_split.append(word)
		card_text = card.get('text', '')
   		dbcreate_cards = Cards(card_name,str(sorted((card_mana_cost_split))), 	  		             
 	  		             card_text)
 	  	db.session.add(dbcreate_cards)
 	 	db.session.commit()

 	# POPULATING COLORS

 	colors = ["Red",
			  "Green",
			  "Blue",
			  "Black",
			  "White"]
	for color in colors:
		dbcreate_colors = Colors(color)
		db.session.add(dbcreate_colors)
		db.session.commit()

	# POPULATING TYPES

	for each in types_flatten:
		dbcreate_types = Types(each)
		db.session.add(dbcreate_types)
		db.session.commit()

	# POPULATING SUBTYPES 

	for subtype in subtypes_flatten:
		dbcreate_subtypes = Subtypes(subtype)
		db.session.add(dbcreate_subtypes)
		db.session.commit()

	# POPULATING CLANS

	clans = ["Azorius",
			 "Dimir",
			 "Rakdos",
		 	 "Gruul",
		   	 "Selesnya",
			 "Orzhov",
			 "Izzet",
			 "Golgari",
			 "Boros",
			 "Simic"]
	for clan in clans:
		dbcreate = Clans(clan)
		db.session.add(dbcreate)
		db.session.commit()

	return 'db is populated'


	# MAPPING CARDS

def map_tests():

	for card in json_test_cards.values():
		subtypes = card.get('subtypes','')
		types = card.get('types', '')
		colors = card.get('colors', '')
		name = card.get('name','')
		table_card = Cards.query.filter_by(name = name).first()
		for color in colors:
			color_table = Colors.query.filter_by(color = color).first()
			table_card.colors_ref.append(color_table)
		for type in types:
			type_table = Types.query.filter_by(types = type).first()
			table_card.types_ref.append(type_table)
		for subtype in subtypes:
			subtype_table = Subtypes.query.filter_by(subtype = subtype).first()
			table_card.subtypes_ref.append(subtype_table)
		db.session.commit()

	

