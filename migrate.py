from app import app,db
from tables import Cards,Colors,Types,Subtypes
from loadjsoncards import data
from allsingletypes import types_flatten, subtypes_flatten
import re
# --------------------------------------------------------------

# THIS ROUTE IS ONLY FOR POPULATING DB WITH CARD FROM JSONFILE

@app.route('/add', methods = ['POST'])
def add_cards():
 	
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
 	return 'added'
# --------------------------------------------------------------

# THIS ROUTE IS ONLY FOR POPULATING DB WITH COLORS

@app.route('/addcolors', methods = ['POST'])
def add_colors():
	colors = ["Red",
			  "Green",
			  "Blue",
			  "Black",
			  "White"]
	for color in colors:
		dbcreate = Colors(color)
		db.session.add(dbcreate)
		db.session.commit()
	return 'added'
# --------------------------------------------------------------

# THIS ROUTE IS FOR RELATING COLORS AND CARDS

@app.route('/mapcolors', methods = ['POST'])
def map_colors():

	for card in data.values():
		colors = card.get('colors', '')
		name = card.get('name','')
		table_card = Cards.query.filter_by(name = name).first()
		for color in colors:
			color_table = Colors.query.filter_by(color = color).first()
			table_card.colorsref.append(color_table)
			db.session.commit()
	return 'ok'
# --------------------------------------------------------------

# THIS ROUTE IS FOR POPULATING DB WITH TYPES

@app.route('/addtypes', methods = ['POST'])
def add_types():

	for type in types_flatten:
		dbcreate = Types(type)
		db.session.add(dbcreate)
		db.session.commit()
	return 'added'
# --------------------------------------------------------------

# THIS ROUTE IS FOR RELATING COLORS AND TYPES

@app.route('/maptypes', methods = ['POST'])
def map_types():

	for card in data.values():
		types = card.get('types', '')
		name = card.get('name', '')
		table_card = Cards.query.filter_by(name = name).first()
		for type in types:
			type_table = Types.query.filter_by(types = type).first()
			table_card.typesref.append(type_table)
			db.session.commit()
	return 'ok'
# --------------------------------------------------------------

# THIS ROUTE IS FOR POPULATING DB WITH SUBTYPES

@app.route('/addsubtypes', methods = ['POST'])
def add_subtypes():

	for subtype in subtypes_flatten:
		dbcreate = Subtypes(subtype)
		db.session.add(dbcreate)
		db.session.commit()
	return 'added'
# --------------------------------------------------------------

# THIS ROUTE IS FOR RELATING COLORS AND SUBTYPES

@app.route('/mapsubtypes', methods = ['POST'])
def map_subtypes():

	for card in data.values():
		subtypes = card.get('subtypes', '')
		name = card.get('name', '')
		table_card = Cards.query.filter_by(name = name).first()
		for subtype in subtypes:
			subtype_table = Subtypes.query.filter_by(subtype = subtype).first()
			table_card.subtypesref.append(subtype_table)
			db.session.commit()
	return 'ok'




# THIS ROUTE IS ONLY FOR INCREMENTING DB WITH CLANS

# @app.route('/addclans', methods = ['POST'])
# def add_clans():
# 	clans = ["Azorius",
# 			 "Dimir",
# 			 "Rakdos",
# 		 	 "Gruul",
# 		   	 "Selesnya",
# 			 "Orzhov",
# 			 "Izzet",
# 			 "Golgari",
# 			 "Boros",
# 			 "Simic"]
# 	for number in range(len(clans)):
# 		dbcreate = Clans(clans[number])
# 		db.session.add(dbcreate)
# 		db.session.commit()
# 	return 'added'
