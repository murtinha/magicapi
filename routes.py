from app import app,db
from tables import Cards, Users, Colors, Types, Subtypes, Clans
from flask import request, jsonify


# HEALTH-CHECK

@app.route('/health-check')
def health_check():
	return 'It lives!!!'

# --------------------------------------------------------------------
# TABLE CARDS ROUTES
# --------------------------------------------------------------

# SHOWING CARDS BY NAME

@app.route('/name/', methods = ['GET'])
def show_card_by_name():

	name = request.args.get('name','')
	card = Cards.query.filter_by(name = name).first()
	card_name = card.name
	card_manacost = card.mana_cost
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
						   text = card_text))
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

@app.route('/colors/')
def show_card_colors():

  	colors = request.args.get('colors', '')
 	colors_list = colors.split(',')
  	cardnames = []
	color_column = Colors.query.filter_by(color = colors_list[0]).first()
	for card in color_column.colorcards:
  		tostring = []
		for color in card.colors_ref:
			tostring.append(str(color))
		if sorted(tostring) == sorted(colors_list):
			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))
# --------------------------------------------------------------

# SHOW CARD USERS

@app.route('/users')
def show_card_users():

	user_input = request.get_json()
	cardname = user_input['name']
	users = Cards.query.filter_by( name = cardname).first()
	usernames = []
	for user in users.owner:
		usernames.append(user.username)
	return jsonify(dict(usernames = usernames))
# --------------------------------------------------------------

# SHOWING CARDS BY TEXT

@app.route('/text')
def show_card_by_text():

	user_input = request.get_json()
	text = user_input['text']
	cards = Cards.query.all()
	cardnames = []
	card_filter = 0
	for card in cards:
		for word in text:
			if word in card.text.lower():
				card_filter = 1
			else:
				card_filter = 0
				break
		if card_filter == 1:
			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES

@app.route('/subtypes')
def show_card_by_subtypes():

	user_input = request.get_json()
	subtypes = user_input['subtypes']
	subtype_column = Subtypes.query.filter_by(subtype = subtypes[0]).first()
	cardnames = []
	subtype_filter= 0 # Guarantee that all subtypes are in the card at once
	for card in subtype_column.subtypescards:
		tostring = []
		for subtype in card.subtypes_ref:
			tostring.append(str(subtype))
		for subtype in subtypes:
			if subtype in tostring:
				subtype_filter = 1
			else:
				subtype_filter = 0
				break
		if subtype_filter == 1:
			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))
	
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES,COLOR,TEXT

@app.route('/subtypes/colors/text')
def show_card_by_sub_color_text():

	user_input = request.get_json()
	subtypes = user_input['subtypes']
	colors = sorted(user_input['colors'])
	text = user_input['text']
	if len(colors) > 0:
		color_column = Colors.query.filter_by(color = colors[0]).first()
	else :
		color_column = Colors.query.filter_by(color = colors).first()
	card_filter_text = 0 
	cardnames = []
	subtype_filter = 0
	for card in color_column.colorcards:
		subtype_tostring = []
		color_tostring = []
		for subtype in card.subtypes_ref:
			subtype_tostring.append(str(subtype))
		for color in card.colors_ref:
			color_tostring.append(str(color))
		if sorted(color_tostring) == colors:
			for subtype in subtypes:
				if subtype in subtype_tostring:
					subtype_filter = 1
				else:
					subtype_filter = 0
					break
			if subtype_filter == 1:
				for word in text:
					if word in card.text.lower():
						card_filter_text = 1
					else:
						card_filter_text = 0
						break
				if card_filter_text == 1:
					cardnames.append(card.name)
	return jsonify(dict(names = cardnames))


# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST

@app.route('/manacost')
def show_card_by_manacost():

	user_input = request.get_json()
	manacost = user_input['mana_cost']
	cardnames = []
	cards = Cards.query.filter_by(mana_cost = str(manacost)).all()
	for card in cards:
		if card.mana_cost == manacost:
			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY TYPES

@app.route('/types')
def show_card_by_types():

	user_input = request.get_json()
	types = user_input['types']
	type_column = Types.query.filter_by(types = types[0]).first()
	cardnames = []
	type_filter = 0
	for card in type_column.typecards:
		tostring = []
		for type in card.types_ref:
			tostring.append(str(type))
		for type in types:
			if type in tostring:
				type_filter = 1
			else:
				type_filter = 0
				break
		if type_filter == 1:
			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))


# --------------------------------------------------------------


# SHOWING CARDS BY MANACOST AND COLOR

@app.route('/manacost/colors')
def show_card_by_mana_color():

	user_input = request.get_json()
	manacost = user_input['mana_cost']
	cardnames = []
	colors = sorted(user_input['colors'])
	card_from_manacost = Cards.query.filter_by( mana_cost = manacost).all()
	for card in card_from_manacost:
		tostring = []
		for color in card.colors_ref:
			tostring.append(str(color))
		if sorted(tostring) == colors:
			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))
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
	return jsonify(dict(names = card_name)) + 'added to %s' % user.username
# --------------------------------------------------------------

# SHOWING USER CARDS

@app.route('/cards/<username>')
def show_user_cards(username):
	cardsnames = []
	user = Users.query.filter_by(username = username).first()
	for card in user.user_cards:
		cardsnames.append(card.name)
	return jsonify(dict(name = cardsnames))
# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST

@app.route('/manacost/<username>')
def show_user_card_by_manacost(username):

	user_input = request.get_json()
	manacost = user_input['mana_cost']
	cardnames = []
	user = Users.query.filter_by(username = username).first()
	for card in user.user_cards:
		if card.mana_cost == manacost:
			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY NAME

@app.route('/name/<username>')
def show_user_card_by_name(username):

	user_input = request.get_json()
	name = user_input['name']
	user = Users.query.filter_by(username = username).first()
	for card in user.user_cards:
		if(card.name == name):
			card_name = card.name
			card_manacost = card.mana_cost
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
						   text = card_text))
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

@app.route('/colors/<username>')
def show_user_card_colors(username):

  	user_input = request.get_json()
  	colors = sorted(user_input['colors'])
  	cardnames = []
  	user = Users.query.filter_by(username = username).first()
	for card in user.user_cards:
  		tostring = []
		for color in card.colors:
			tostring.append(str(color))
		if sorted(tostring) == colors:
			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))

# --------------------------------------------------------------

# SHOWING CARDS BY TYPES

@app.route('/types/<username>')
def show_user_card_by_types(username):

	user_input = request.get_json()
	types = user_input['types']
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	type_filter = 0
	for card in user.user_cards:
		tostring = []
		for type in card.types:
			tostring.append(str(type))
		for type in types:
			if types in tostring:
				type_filter = 1 
			else:
				type_filter = 0
				break
		if type_filter == 1:
			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY TEXT

@app.route('/text/<username>')
def show_user_card_by_text(username):

	user_input = request.get_json()
	text = user_input['text']
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	card_filter = 0
	for card in user.user_cards:
		for word in text:
			if word in card.text.lower():
				card_filter = 1
			else:
				card_filter = 0
				break
		if card_filter == 1:
			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES

@app.route('/subtypes/<username>')
def show_user_card_by_subtypes(username):

	user_input = request.get_json()
	subtypes = user_input['subtypes']
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	subtype_filter= 0 # Guarantee that all subtypes are in the card at once
	for card in user.user_cards:
		tostring = []
		for subtype in card.subtypes:
			tostring.append(str(subtype))
		for subtype in subtypes:
 			if subtype in tostring: 
 				subtype_filter = 1
 			else:
 				subtype_filter = 0
 				break
 		if subtype_filter == 1:
 			cardnames.append(card.name)
	return jsonify(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST AND COLOR

@app.route('/manacost/colors/<username>')
def show_user_card_by_mana_color(username):

	user_input = request.get_json()
	manacost = user_input['mana_cost']
	cardnames = []
	colors = user_input['colors']
	user = Users.query.filter_by(username = username).first()
	for eachcard in user.user_cards:		
		if eachcard.mana_cost == manacost:
			if eachcard.colors == str(sorted(colors)):
				cardnames.append(eachcard.name)
	return jsonify(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES,COLOR,TEXT

@app.route('/subtypes/colors/text/<username>')
def show_user_card_by_sub_color_text(username):

	user_input = request.get_json()
	subtypes = user_input['subtypes']
	colors = sorted(user_input['colors'])
	text = user_input['text']
	user = Users.query.filter_by(username = username).first()
	card_filter_text = 0 
	cardnames = []
	subtype_filter = 0
	for card in user.user_cards:
		subtype_tostring = []
		color_tostring = []
		for subtype in card.subtypes:
			subtype_tostring.append(str(subtype))
		for color in card.colors:
			color_tostring.append(str(color))
		if sorted(color_tostring) == colors:
			for subtype in subtypes:
				if subtype in subtype_tostring:
					subtype_filter = 1
				else:
					subtype_filter = 0
					break
			if subtype_filter == 1:
				for word in text:
					if word in card.text.lower():
						card_filter_text = 1
					else:
						card_filter_text = 0
						break
				if card_filter_text == 1:
					cardnames.append(card.name)
	return jsonify(dict(names = cardnames))
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

# @app.route('/delete/card/<username>')
# def delete_card_from_user(username):
	
# 	  user_input = request.get_json()
# 	  cardname = user_input['name']
# 	user = Users.query.filter_by(username = username).first()
# 	print user.user_cards
# 	return 'ok'	


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
