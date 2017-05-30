from flask import json
from magic import app,db
from magic.models.tables import *
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
types_flatten.append("empty")

for subtype in subtypes:
	subtypes_flatten += tuple(subtype)
subtypes_flatten = list(set(subtypes_flatten))
subtypes_flatten.append("empty")




def populate_tests():

	# POPULATING CARDS

	for card in json_test_cards.values():
		card_name = card.get('name', '')
		card_mana_cost = re.sub("\W", "",card.get('manaCost', ''))
		if card_mana_cost != '':
			card_mana_cost = sorted(card_mana_cost)
			card_mana_cost = ''.join(card_mana_cost)
		card_url = card.get('url','')
		card_text = card.get('text', '')
		dbcreate = Cards(card_name,card_mana_cost,card_url,card_text)
  		db.session.add(dbcreate)
 		db.session.commit()

 	# POPULATING COLORS

 	colors = ["Red",
			  "Green",
			  "Blue",
			  "Black",
			  "White",
			  "empty"]
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
		dbcreate_clans = Clans(clan)
		db.session.add(dbcreate_clans)
		db.session.commit()

	return 'db is populated'


	# MAPPING CARDS

def map_tests():

	for card in json_test_cards.values():
		colors = card.get('colors', [])
		name = card.get('name','')
		table_card = Cards.query.filter_by(name = name).first()
		if colors != []:
			for color in colors:
				color_table = Colors.query.filter_by(color = color).first()
				table_card.colors_ref.append(color_table)
		else:
			color_table = Colors.query.filter_by(color = "empty").first()
			table_card.colors_ref.append(color_table)
		db.session.commit()

	for card in json_test_cards.values():
		types = card.get('types', [])
		name = card.get('name', '')
		table_card = Cards.query.filter_by(name = name).first()
		if types != []:
			for type in types:
				type_table = Types.query.filter_by(types = type).first()
				table_card.types_ref.append(type_table)
		else:
			type_table = Types.query.filter_by(types = "empty").first()
			table_card.types_ref.append(type_table)
		db.session.commit()	

	for card in json_test_cards.values():
		subtypes = card.get('subtypes', [])
		name = card.get('name', '')
		table_card = Cards.query.filter_by(name = name).first()
		if subtypes != []:
			for subtype in subtypes:
				subtype_table = Subtypes.query.filter_by(subtype = subtype).first()
				table_card.subtypes_ref.append(subtype_table)
		else:
			subtype_table = Subtypes.query.filter_by(subtype = "empty").first()
			table_card.subtypes_ref.append(subtype_table)
		db.session.commit()	
	
	return 'mapped'
	

