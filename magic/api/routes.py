from magic import *
from magic.models.tables import Cards, Users, Colors, Types, Subtypes, Clans
from flask import request, jsonify
import re


# HEALTH-CHECK

@app.route('/health-check')
def health_check():
	return 'It lives!!!'

# --------------------------------------------------------------------
# TABLE CARDS ROUTES
# --------------------------------------------------------------


@app.route('/')
def welcome_page():
	return 'WELCOME TO MAGICAPI'

# SHOWING CARDS BY NAME

@app.route('/name/', methods = ['GET'])
def show_card_by_name():

	name = request.args.get('name','')
	card = Cards.query.filter_by(name = name).first()
	card_name = card.name
	card_manacost = card.mana_cost
	card_url = card.img_url
	card_text = card.text
	if type(card.colors_ref) != "None":
		card_colors = str(card.colors_ref)
	else:
		card_colors = "None"
	card_types = str(card.types_ref)
	card_subtypes = str(card.subtypes_ref)
	return jsonify(dict(name = card_name,
						mana_cost = card_manacost,
						colors = card_colors,
						types = card_types,
						subtypes = card_subtypes,
						img_url = card_url,
						text = card_text))
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

@app.route('/colors/')
def show_card_colors():

  	colors = request.args.get('colors', '')
  	page = int(request.args.get('page', 1))
 	colors_list = colors.split(',')
 	print colors_list
  	last_card = (page*100)+1
	color_t= Colors.query.filter_by(color = colors_list[0]).first()
	if page > 1:
		first_card = last_card - 101
	else:
		first_card = 0
  	cardnames = []
  	cardurl = []
	for card in color_t.colorcards:
  		tostring = []
		for color in card.colors_ref:
			tostring.append(str(color))
		if sorted(tostring) == sorted(colors_list):
			cardnames.append(card.name)
			cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames[first_card:last_card], url = cardurl[first_card:last_card]))
# --------------------------------------------------------------

# SHOW CARD USERS

@app.route('/users/')
def show_card_users():

	cardname = request.args.get('name','')
	users = Cards.query.filter_by( name = cardname).first()
	usernames = []
	for user in users.owner:
		usernames.append(user.username)
	return jsonify(dict(usernames = usernames))
# --------------------------------------------------------------

# SHOWING CARDS BY TEXT

@app.route('/text/')
def show_card_by_text():

	text = request.args.get('text','')
	text_list = text.split(',')
	cards = Cards.query.all()
	cardnames = []
	cardurl = []
	card_filter = 0
	for card in cards:
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

@app.route('/subtypes/')
def show_card_by_subtypes():

	subtypes = request.args.get('subtypes','')
	subtypes_list = subtypes.split(',')
	subtype_column = Subtypes.query.filter_by(subtype = subtypes_list[0]).first()
	cardnames = []
	cardurl = []
	subtype_filter= 0 # Guarantee that all subtypes are in the card at once
	for card in subtype_column.subtypescards:
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
	return jsonify(dict(names = cardnames, url = cardurl))
	
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR,TEXT

@app.route('/colors/text/')
def show_card_by_sub_color_text():

	args = request.args
	colors = request.args.get('colors','')
	colors_list = colors.split(',')
	if len(colors_list) > 1:
		colors_list = sorted(colors_list)
	text = request.args.get('text','')
	text_list = text.split(',')
	color_column = Colors.query.filter_by(color = colors_list[0]).first()
	card_filter_text = 0 
	cardnames = []
	cardurl = []
	subtype_filter = 0
	for card in color_column.colorcards:
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

# SHOWING CARDS BY MANACOST

@app.route('/manacost/')
def show_card_by_manacost():

	manacost = request.args.get('manacost','')
	manacost_sorted = sorted(manacost)
	manacost_sorted = ''.join(manacost_sorted)
	cardnames = []
	cardurl = []
	cards = Cards.query.filter_by(mana_cost = manacost_sorted).all()
	for card in cards:
		cardnames.append(card.name)
		cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames,url = cardurl))
# --------------------------------------------------------------

# SHOWING CARDS BY TYPES

@app.route('/types/')
def show_card_by_types():

	types = request.args.get('types','')
	types_list = types.split(',')
	type_column = Types.query.filter_by(types = types_list[0]).first()
	cardnames = []
	cardurl = []
	type_filter = 0
	for card in type_column.typecards:
		tostring = []
		for type in card.types_ref:
			tostring.append(str(type))
		for type in types_list:
			if type in tostring:
				type_filter = 1
			else:
				type_filter = 0
				break
		if type_filter == 1:
			cardnames.append(card.name)
			cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames, url = cardurl))


# --------------------------------------------------------------


# SHOWING CARDS BY MANACOST AND COLOR

@app.route('/manacost/colors/')
def show_card_by_mana_color():

	manacost = request.args.get('manacost','')
	cardnames = []
	cardurl = []
	colors = request.args.get('colors','')
	colors_list = colors.split(',')
	if len(colors_list) > 1:
		colors_list = sorted(colors_list)
	card_from_manacost = Cards.query.filter_by( mana_cost = manacost).all()
	for card in card_from_manacost:
		tostring = []
		for color in card.colors_ref:
			tostring.append(str(color))
		if sorted(tostring) == colors_list:
			cardnames.append(card.name)
			cardurl.append(card.img_url)
	return jsonify(dict(names = cardnames, url = cardurl))
# --------------------------------------------------------------


# --------------------------------------------------------------
# TABLE USERS ROUTES
# --------------------------------------------------------------

# ADDING USER

@app.route('/adduser', methods = ['POST'])
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

@app.route('/addcard/<username>', methods = ['POST'])
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

@app.route('/cards/<username>')
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

@app.route('/manacost/<username>/')
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

@app.route('/name/<username>/')
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

@app.route('/colors/<username>/')
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

@app.route('/types/<username>/')
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

@app.route('/text/<username>/')
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

@app.route('/subtypes/<username>/')
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

@app.route('/manacost/colors/<username>/')
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

@app.route('/colors/text/<username>/')
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

@app.route('/delete/<username>', methods = ['DELETE'])
def delete_user(username):
	
	user = Users.query.filter_by(username = username).first()
	user_id = user.user_id
	db.session.delete(user)
	db.session.commit()
	return 'User with id = %d deleted' % user_id
# --------------------------------------------------------------

# DELETING CARD FROM USER

@app.route('/delete/card/<username>', methods = ['DELETE'])
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
		


# --------------------------------------------------------------
# TABLE CLANS ROUTES
# --------------------------------------------------------------

# ADDING USER TO CLAN

@app.route('/addclan/<username>', methods = ['POST'])
def add_user_to_clan(username):

	user_input = request.get_json()
	userclan = user_input['clan']
	user = Users.query.filter_by(username = username).first()
	if user.myclan == None:
	 	clan_ref = Clans.query.filter_by(clan_name = userclan).first()
	 	clan_ref.user_ref.append(user)
		db.session.commit()
	else:
		my_clan = Clans.query.filter_by(clan_id = user.my_clan).first()
		return 'You already have a clan (%s)!' % my_clan.clan_name
	return 'Clan %s added to User %s' % (clan_ref.clan_name, user.username)
# --------------------------------------------------------------

# SHOWING USER CLAN

@app.route('/clan/<username>')
def show_user_clan(username):

	user = Users.query.filter_by(username = username).first()
	clan_id = user.my_clan
	clan = Clans.query.filter_by(clan_id = clan_id).first()

	return 'Your clan is %s' % clan.clan_name
# --------------------------------------------------------------

# SHOWING CLAN USERS

@app.route('/clan/users/<clanname>')
def show_clan_users(clanname):

	clan = Clans.query.filter_by(clan_name = clanname).first()
	clan_id = clan.clan_id
	users = Users.query.filter_by(my_clan = clan_id).all()
	user_names = []
	for user in users:
		user_names.append(user.username)
	return jsonify(dict(users = user_names))
# --------------------------------------------------------------

# UPDATING USER CLAN

@app.route('/clan/update/<username>', methods = ['PUT'])
def update_clan_users(username):

	user_input = request.get_json()
	clan = user_input['clan']
	user = Users.query.filter_by(username = username).first()
	old_clan = Clans.query.filter_by(clan_id = user.my_clan).first()
	old_clan_name = old_clan.clan_name 
	new_clan = Clans.query.filter_by(clan_name = clan).first()
	new_clan.user_ref.append(user)
	db.session.commit()
	return 'You changed from %s to %s' % (old_clan_name,clan)
# --------------------------------------------------------------
