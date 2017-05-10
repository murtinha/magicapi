from app import app,db
from tables import Cards,Colors,Types,Subtypes, Clans
from loadjsoncards import data
from allsingletypes import types_flatten, subtypes_flatten
import re
# --------------------------------------------------------------

# THIS ROUTE IS ONLY FOR POPULATING DB WITH CARD FROM JSONFILE

 	
for card in data.values():
	card_name = card.get('name', '')
	card_mana_cost = re.sub("\W", "",card.get('manaCost', ''))
	card_mana_cost_split = []
	for word in card_mana_cost:
		card_mana_cost_split.append(word)
	card_text = card.get('text', '')
	dbcreate = Cards(card_name,str(sorted((card_mana_cost_split))), 	  		             
 		             card_text)
  	db.session.add(dbcreate)
 	db.session.commit()

colors = ["Red",
		  "Green",
		  "Blue",
		  "Black",
		  "White"]
for color in colors:
	dbcreate = Colors(color)
	db.session.add(dbcreate)
	db.session.commit()

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

for card in data.values():
	colors = card.get('colors', None)
	name = card.get('name','')
	table_card = Cards.query.filter_by(name = name).first()
	if colors != None:
		for color in colors:
			color_table = Colors.query.filter_by(color = color).first()
			table_card.colors_ref.append(color_table)
			db.session.commit()

for type in types_flatten:
	dbcreate = Types(type)
	db.session.add(dbcreate)
	db.session.commit()

for card in data.values():
	types = card.get('types', None)
	name = card.get('name', '')
	table_card = Cards.query.filter_by(name = name).first()
	if types != None:
		for type in types:
			type_table = Types.query.filter_by(types = type).first()
			table_card.types_ref.append(type_table)
			db.session.commit()

for subtype in subtypes_flatten:
	dbcreate = Subtypes(subtype)
	db.session.add(dbcreate)
	db.session.commit()


for card in data.values():
	subtypes = card.get('subtypes', None)
	name = card.get('name', '')
	table_card = Cards.query.filter_by(name = name).first()
	if subtypes != None:
		for subtype in subtypes:
			subtype_table = Subtypes.query.filter_by(subtype = subtype).first()
			table_card.subtypes_ref.append(subtype_table)
			db.session.commit()



