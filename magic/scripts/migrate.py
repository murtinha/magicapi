from magic import app,db
from magic.models.tables import Cards,Colors,Types,Subtypes, Clans
from jsoncards import data_json
from allsingletypes import single_types, single_subtypes
import re
# --------------------------------------------------------------

# THIS ROUTE IS ONLY FOR POPULATING DB WITH CARD FROM JSONFILE

types_flatten = single_types(data_json)
subtypes_flatten = single_subtypes(data_json)

# CARDS
 	
for card in data_json.values():
	card_name = card.get('name', '')
	card_mana_cost = re.sub("\W", "",card.get('manaCost', ''))
	if card_mana_cost != '':
		card_mana_cost = sorted(card_mana_cost)
		card_mana_cost = ''.join(card_mana_cost)
	card_url = card.get('url','')
	card_text = card.get('text', '')
	dbcreate = Cards(card_name,card_mana_cost, 	  		             
 		             card_url,card_text)
  	db.session.add(dbcreate)
 	db.session.commit()
# --------------------------------------------------------------

# COLORS

colors = ["Red",
		  "Green",
		  "Blue",
		  "Black",
		  "White",
		  "empty"]

for color in colors:
	dbcreate = Colors(color)
	db.session.add(dbcreate)
	db.session.commit()

for card in data_json.values():
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
# --------------------------------------------------------------

# CLANS

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
# --------------------------------------------------------------

# TYPES

for type in types_flatten:
	dbcreate = Types(type)
	db.session.add(dbcreate)
	db.session.commit()

for card in data_json.values():
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
# --------------------------------------------------------------

# SUBTYPES

for subtype in subtypes_flatten:
	dbcreate = Subtypes(subtype)
	db.session.add(dbcreate)
	db.session.commit()


for card in data_json.values():
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



