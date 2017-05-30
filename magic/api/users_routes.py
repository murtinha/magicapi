from magic import db
from magic.models.tables import Cards, Users, Colors, Types, Subtypes
from flask import request, jsonify, Blueprint
import re

users_blueprint = Blueprint('users_routes', __name__)

# --------------------------------------------------------------
# TABLE USERS ROUTES
# --------------------------------------------------------------

# ADDING USER

@users_blueprint.route('/adduser', methods = ['POST'])
def add_user():

	user_input = request.get_json()
	user_username = user_input['username']
	user_email = user_input['email']
	dbcreate = Users(user_username, user_email)

	db.session.add(dbcreate)
	db.session.commit()

	return 'User %s added' % user_username
# --------------------------------------------------------------

# ADDING CARDS TO A SPECIFIC USER

@users_blueprint.route('/addcard/<username>', methods = ['POST'])
def add_card_to_user(username):

	user_input = request.get_json()
	card_name = user_input['name']
	user = Users.query.filter_by(username = username).first()
	for number in range(len(card_name)):
		card = Cards.query.filter_by(name = card_name[number]).first()
		card.owner.append(user)
		db.session.commit()
	return jsonify(dict(names = card_name))
# --------------------------------------------------------------

# SHOWING USER CARDS

@users_blueprint.route('/cards/<username>')
def show_user_cards(username):
	cardsnames = []
	cardurl = []
	user = Users.query.filter_by(username = username).first()
	for card in user.user_cards:
		cardsnames.append(card.name)
		cardurl.append(card.img_url)
	return jsonify(dict(names = cardsnames, url = cardurl))
# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST

@users_blueprint.route('/manacost/<username>/')
def show_user_card_by_manacost(username):

	manacost = request.args.get('manacost','')
	manacost_sorted = sorted(manacost)
	manacost_sorted = ''.join(manacost_sorted)
	cardnames = []
	cardurl = []
	user = Users.query.filter_by(username = username).first()
	for card in user.user_cards:
		if card.mana_cost == manacost_sorted:
			cardnames.append(card.name)
			cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames, url = cardurl))
# --------------------------------------------------------------

# SHOWING CARDS BY NAME

@users_blueprint.route('/name/<username>/')
def show_user_card_by_name(username):

	name = request.args.get('name','')
	user = Users.query.filter_by(username = username).first()
	for card in user.user_cards:
		if(card.name == name):
			card_name = card.name
			card_manacost = card.mana_cost
			card_url = card.img_url
			card_text = card.text
			card_colors = str(card.colors_ref)
			card_types = str(card.types_ref)
			card_subtypes = str(card.subtypes_ref)
			break
	return jsonify(dict(name = card_name,
						   mana_cost = card_manacost,
						   colors = card_colors,
						   types = card_types,
						   subtypes = card_subtypes,
						   img_url = card_url,
						   text = card_text))
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

@users_blueprint.route('/colors/<username>/')
def show_user_card_colors(username):

  	colors = request.args.get('colors','')
  	colors_list = colors.split(',')
  	if len(colors_list) > 1:
  		colors_list = sorted(colors_list)
  	cardnames = []
  	cardurl = []
  	user = Users.query.filter_by(username = username).first()
	for card in user.user_cards:
  		tostring = []
		for color in card.colors_ref:
			tostring.append(str(color))
		if sorted(tostring) == colors_list:
			cardnames.append(card.name)
			cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames, url = cardurl))

# --------------------------------------------------------------

# SHOWING CARDS BY TYPES

@users_blueprint.route('/types/<username>/')
def show_user_card_by_types(username):

	types = request.args.get('types','')
	types_list = types.split(',')
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	cardurl = []
	type_filter = 0
	for card in user.user_cards:
		tostring = []
		for type in card.types_ref:
			tostring.append(str(type))
		for type in types_list:
			if types in tostring:
				type_filter = 1 
			else:
				type_filter = 0
				break
		if type_filter == 1:
			cardnames.append(card.name)
			cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames, url = cardurl))
# --------------------------------------------------------------

# SHOWING CARDS BY TEXT

@users_blueprint.route('/text/<username>/')
def show_user_card_by_text(username):

	text = request.args.get('text','')
	text_list = text.split(',')
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	cardurl = []
	card_filter = 0
	for card in user.user_cards:
		split_text = re.split(r'\s+|[,;.-]\s*', card.text.lower())
		for word in text_list:
			if word in split_text:
				card_filter = 1
			else:
				card_filter = 0
				break
		if card_filter == 1:
			cardnames.append(card.name)
			cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames, url = cardurl))
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES

@users_blueprint.route('/subtypes/<username>/')
def show_user_card_by_subtypes(username):

	subtypes = request.args.get('subtypes','')
	subtypes_list = subtypes.split(',')
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	cardurl = []
	subtype_filter= 0 # Guarantee that all subtypes are in the card at once
	for card in user.user_cards:
		tostring = []
		for subtype in card.subtypes_ref:
			tostring.append(str(subtype))
		for subtype in subtypes_list:
 			if subtype in tostring: 
 				subtype_filter = 1
 			else:
 				subtype_filter = 0
 				break
 		if subtype_filter == 1:
 			cardnames.append(card.name)
 			cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames, url =cardurl))
# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST AND COLOR

@users_blueprint.route('/manacost/colors/<username>/')
def show_user_card_by_mana_color(username):

	manacost = request.args.get('manacost','')
	manacost_sorted = sorted(manacost)
	manacost_sorted = ''.join(manacost_sorted)
	cardnames = []
	cardurl = []
	colors = request.args.get('colors','')
	colors_list = colors.split(',')
	if len(colors_list) > 1:
		colors_list = sorted(colors_list)
	user = Users.query.filter_by(username = username).first()
	for eachcard in user.user_cards:		
		tostring = []
		for color in eachcard.colors_ref:
			tostring.append(str(color))
		if eachcard.mana_cost == manacost_sorted:
			if tostring == colors_list:
				cardnames.append(eachcard.name)
				cardurl.append(eachcard.img_url)
	return jsonify(dict(names = cardnames, url = cardurl))
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR,TEXT

@users_blueprint.route('/colors/text/<username>/')
def show_user_card_by_sub_color_text(username):

	colors = request.args.get('colors','')
	colors_list = colors.split(',')
	if len(colors_list) > 1:
		colors_list = sorted(colors_list)
	text = request.args.get('text','')
	text_list = text.split(',')
	user = Users.query.filter_by(username = username).first()
	card_filter_text = 0 
	cardnames = []
	cardurl = []
	for card in user.user_cards:
		color_tostring = []
		for color in card.colors_ref:
			color_tostring.append(str(color))
		if sorted(color_tostring) == colors_list:
			split_text = re.split(r'\s+|[,;.-]\s*', card.text.lower())
			for word in text_list:
				if word in split_text:
					card_filter_text = 1
				else:
					card_filter_text = 0
					break
			if card_filter_text == 1:
				cardnames.append(card.name)
				cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames, url = cardurl))
# --------------------------------------------------------------

# DELETING USER

@users_blueprint.route('/delete/<username>', methods = ['DELETE'])
def delete_user(username):
	
	user = Users.query.filter_by(username = username).first()
	user_id = user.user_id
	db.session.delete(user)
	db.session.commit()
	return 'User with id = %d deleted' % user_id
# --------------------------------------------------------------

# DELETING CARD FROM USER

@users_blueprint.route('/delete/card/<username>', methods = ['DELETE'])
def delete_card_from_user(username):
	
	user_input = request.get_json()
	cardname = user_input['name']
	user = Users.query.filter_by(username = username).first()
	card_check = 0
	for card in user.user_cards:
		if card.name == cardname:
			card_check = 1
			user.user_cards.remove(card)
			db.session.commit()
		return '%s removed from user %s' % (cardname, user.username)			
	if card_check == 0 :
		return '%s was not found in user %s' % (cardname, user.username)
		