from app import app,db
from tables import Cards, Users, Colors, Types, Subtypes
from flask import request, json


# HEALTH-CHECK

@app.route('/health-check')
def health_check():
	subtypes = ''
	return 'It lives!!!'

# --------------------------------------------------------------------
# TABLE CARDS ROUTES
# --------------------------------------------------------------

# SHOWING CARDS BY NAME

@app.route('/name')
def show_card_by_name():

	user_input = request.get_json()
	name = user_input['name']
	card = Cards.query.filter_by(name = name).first()
	card_name = card.name
	card_manacost = card.mana_cost
	card_text = card.text
	card_colors = str(card.colorsref)
	card_types = str(card.typesref)
	card_subtypes = str(card.subtypesref)
	return json.dumps(dict(name = card_name,
						   mana_cost = card_manacost,
						   colors = card_colors,
						   types = card_types,
						   subtypes = card_subtypes,
						   text = card_text))
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

@app.route('/colors')
def show_card_colors():

  	user_input = request.get_json()
  	colors = sorted(user_input['colors'])
  	cardnames = []
	color_column = Colors.query.filter_by(color = colors[0]).first()
	for card in color_column.colorcards:
		tostring = []
		for color in card.colors:
			tostring.append(str(color))
		if sorted(tostring) == colors:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
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
	return json.dumps(dict(usernames = usernames))
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
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES

@app.route('/subtypes')
def show_card_by_subtypes():

	user_input = request.get_json()
	subtypes = sorted(user_input['subtypes'])
	subtype_column = Subtypes.query.filter_by(subtype = subtypes[0]).first()
	cardnames = []
	card_filter= 0 # Guarantee that all subtypes are in the card at once
	for card in subtype_column.subtypescards:
		tostring = []
		for subtype in card.subtypes:
			tostring.append(str(subtype))
		if sorted(tostring) == subtypes:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
	
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES,COLOR,TEXT

@app.route('/subtypes/colors/text')
def show_card_by_sub_color_text():

	user_input = request.get_json()
	subtypes = sorted(user_input['subtypes'])
	colors = sorted(user_input['colors'])
	text = user_input['text']
	color_column = Colors.query.filter_by(color = colors[0]).first()
	card_filter_text = 0 
	cardnames = []
	for card in color_column.colorcards:
		subtype_tostring = []
		color_tostring = []
		for subtype in card.subtypes:
			subtype_tostring.append(str(subtype))
		for color in card.colors:
			color_tostring.append(str(color))
		if ( sorted(subtype_tostring) == subtypes ) & ( sorted(color_tostring) == colors ):
			for word in text:
				if word in card.text.lower():
					card_filter_text = 1
				else:
					card_filter_text = 0
					break
			if card_filter_text == 1:
				cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))


# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST

@app.route('/manacost')
def show_card_by_manacost():

	user_input = request.get_json()
	manacost = user_input['mana_cost']
	formated_manacost = ''
	cardnames = []
	for letter in manacost:
		formated_manacost += '{%s}' % letter # To get input in {letter}{letter} format
	card = Cards.query.filter_by(mana_cost = formated_manacost).all()
	for number in range(len(card)):
		cardnames.append(card[number].name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY TYPES

@app.route('/types')
def show_card_by_types():

	user_input = request.get_json()
	types = sorted(user_input['types'])
	type_column = Types.query.filter_by(types = types[0]).first()
	cardnames = []
	for card in type_column.typecards:
		tostring = []
		for type in card.types:
			tostring.append(str(type))
		if sorted(tostring) == types:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))


# --------------------------------------------------------------


# SHOWING CARDS BY MANACOST AND COLOR

@app.route('/manacost/colors')
def show_card_by_mana_color():

	user_input = request.get_json()
	manacost = user_input['mana_cost']
	formated_manacost = ''
	cardnames = []
	for letter in manacost:
		formated_manacost += '{%s}' % letter # To get input in {letter}{letter} format
	colors = sorted(user_input['colors'])
	card_from_manacost = Cards.query.filter_by( mana_cost = formated_manacost).all()
	for card in card_from_manacost:
		tostring = []
		for color in card.colors:
			tostring.append(str(color))
		if sorted(tostring) == colors:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
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

@app.route('/add/<username>', methods = ['POST'])
def add_card_to_user(username):

	user_input = request.get_json()
	card_name = user_input['name']
	user = Users.query.filter_by(username = username).first()
	for number in range(len(card_name)):
		card = Cards.query.filter_by(name = card_name[number]).first()
		card.owner.append(user)
		db.session.commit()
	return json.dumps(dict(names = card_name)) + 'added to %s' % user.username
# --------------------------------------------------------------

# SHOWING USER CARDS

@app.route('/cards/<username>')
def show_user_cards(username):
	cardsnames = []
	user = Users.query.filter_by(username = username).first()
	mycards = user.mycards
	for card in mycards:
		cardsnames.append(card.name)
	return json.dumps(dict(name = cardsnames))
# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST

@app.route('/manacost/<username>')
def show_user_card_by_manacost(username):

	user_input = request.get_json()
	manacost = user_input['manaCost']
	formated_mana_cost = ''
	cardnames = []
	for each in manacost:
		formated_mana_cost += '{%s}' % each # To get input in {letter}{letter} format
	user = Users.query.filter_by(username = username).first()
	for card in user.mycards:
		if card.manaCost == formated_mana_cost:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY NAME

@app.route('/name/<username>')
def show_user_card_by_name(username):

	user_input = request.get_json()
	name = user_input['name']
	cardnames = []
	user = Users.query.filter_by(username = username).first()
	for each in name:
		for card in user.mycards:
			if card.name == each:
				cardnames.append(card)
	return str(cardnames)
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

@app.route('/colors/<username>')
def show_user_card_colors(username):

  	user_input = request.get_json()
  	colors = sorted(user_input['colors'])
  	cardnames = []
  	user = User.query.filter_by(user = username).first()
	for card in user.mycards:
		if card.colors == str(colors):
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))

# --------------------------------------------------------------

# SHOWING CARDS BY TYPES

@app.route('/types/<username>')
def show_user_card_by_types(username):

	user_input = request.get_json()
	types = user_input['types']
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	card_filter = 0
	for card in user.mycards:
		for each in types:
			if each in card.types:
				card_filter = 1
			else:
				card_filter = 0
				break
		if card_filter == 1:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY TEXT

@app.route('/text/<username>')
def show_user_card_by_text(username):

	user_input = request.get_json()
	text = user_input['text']
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	card_filter = 0
	for card in user.mycards:
		for word in text:
			if word in card.text.lower():
				card_filter = 1
			else:
				card_filter = 0
				break
		if card_filter == 1:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES

@app.route('/subtypes/<username>')
def show_user_card_by_subtypes():

	user_input = request.get_json()
	if len(user_input) > 1:
		subtypes = sorted(user_input['subtypes'])
	else:
		subtypes = user_input['subtypes']
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	card_filter= 0 # Guarantee that all subtypes are in the card at once
	for card in user.mycards:
		if card.subtypes != '':
			for subtype in subtypes:
	 			if subtype in card.subtypes: 
	 				card_filter = 1
	 			else:
	 				card_filter = 0
	 				break
	 		if card_filter == 1:
	 			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST AND COLOR

@app.route('/manacost/colors/<username>')
def show_user_card_by_mana_color(username):

	user_input = request.get_json()
	manacost = user_input['manaCost']
	formated_manacost = ''
	cardnames = []
	for eachletter in manacost:
		formated_manacost += '{%s}' % eachletter # To get input in {letter}{letter} format
	colors = user_input['colors']
	user = Users.query.filter_by(username = username).first()
	for eachcard in user.mycards:		
		if eachcard.manaCost == formated_manacost:
			if eachcard.colors == str(sorted(colors)):
				cardnames.append(eachcard.name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES,COLOR,TEXT

@app.route('/subtypes/colors/text/<username>')
def show_user_card_by_sub_color_text(username):

	user_input = request.get_json()
	subtypes = user_input['subtypes']
	colors = sorted(user_input['colors'])
	text = user_input['text']
	user = Users.query.filter_by(username = username).first()
	card_filter_subtype = 0
	card_filter_text = 0 
	cardnames = []
	for card in user.mycards:
		if card.colors == str(colors):
			for subtype in subtypes:
				if str(subtype) in card.subtypes:
					card_filter_subtype = 1
				else:
					card_filter_subtype = 0
					break
			if card_filter_subtype == 1:
				for word in text:
					if word in card.text.lower():
						card_filter_text = 1
					else:
						card_filter_text = 0
						break
				if card_filter_text == 1:
					cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# --------------------------------------------------------------
# TABLE CLANS ROUTES
# --------------------------------------------------------------

# ADDING USER TO CLAN

# @app.route('/addclan/<username>', methods = ['POST'])
# def add_user_to_clan(username):

# 	user_input = request.get_json()
# 	userclan = user_input['clan']
# 	user = Users.query.filter_by(username = username).first()
# 	clan = Clans.query.filter_by(clan_name = userclan).first()
# 	print type(clan)
# 	db.session.commit()
# 	return 'ok'



# --------------------------------------------------------------

# DELETING CLAN

# @app.route('/delete', methods = ['DELETE'])
# def delete_user():
# 	user_input = request.get_json()
# 	cid = user_input['id']
# 	user = Clans.query.filter_by(clan_id = cid).first()
# 	db.session.delete(user)
# 	db.session.commit()
# 	return 'deleted'