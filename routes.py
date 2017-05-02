from app import app,db
from loadjsoncards import data
from tables import Cards, Users
from flask import request, json

# --------------------------------------------------------------

# THIS ROUTE IS ONLY FOR INCREMENTING DB WITH CARD FROM JSONFILE
# DB IS ALREADY INCREMENTED

# @app.route('/add', methods = ['POST'])
# def add_cards():
 	
#  	for card in data.values():
#  		card_name =''
#  		card_manaCost = ''
#  		card_colors = []
#  		card_types = []
#  		card_text = ''
#  		card_subtypes = ''
#  		if 'name' in card:
#  			card_name = card['name']
#  		if 'manaCost' in card:
#  			card_manaCost = card['manaCost']
#  		if 'colors' in card:
#  			card_colors = card['colors']
#  		if 'types' in card:
#  			card_types = card['types']
#  		if 'text' in card:
#  			card_text = card['text']
#  		if 'subtypes' in card:
#  			card_subtypes = card['subtypes']
#    		dbcreate = Cards(card_name,card_manaCost,
#  	  		             str(sorted(card_colors)),str(sorted(card_types)),
#  	  		             str(sorted(card_subtypes)),card_text)
#  	  	db.session.add(dbcreate)
#  	 	db.session.commit()
#  	return 'added'
# --------------------------------------------------------------








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
	names = user_input['name']
	card_list = []
	for name in names:
		cards = Cards.query.filter_by(name = name).first()
		card_list.append(cards)
	return str(card_list)
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

@app.route('/colors')
def show_card_colors():

  	user_input = request.get_json()
  	colors = sorted(user_input['colors'])
  	card_list = []
  	cards = Cards.query.filter_by(colors = str(colors)).all()
	for card in cards:
		card_list.append(card.name)
	print len(card_list)
	return json.dumps(dict(names = card_list))
# --------------------------------------------------------------

# SHOW CARD USERS

@app.route('/users')
def show_card_users():

	user_input = request.get_json()
	card = user_input['name']
	users = Cards.query.filter_by( name = card).first()
	usernames = []
	for user in users.owner:
		usernames.append(user.username)
	return json.dumps(dict(usernames = usernames))
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES

@app.route('/subtypes')
def show_card_by_subtypes():

	user_input = request.get_json()
	if len(user_input) > 1:
		subtypes = sorted(user_input['subtypes'])
	else:
		subtypes = user_input['subtypes']
	print subtypes
	cards = Cards.query.all()
	cardnames = []
	for card in cards:
		if card.subtypes != '':
	 		if str(subtypes) in card.subtypes:
	 			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
	
# --------------------------------------------------------------

# SHOWING CARDS BY SUBTYPES,COLOR,TEXT

# @app.route('/subtypes/colors/text')
# def show_card_by_sub_color_text():

# 	user_input = request.get_json()
# 	subtypes = user_input['subtypes']
# 	colors = user_input['colors']
# 	text = user_input['text']
# 	card_color = Cards.query.filter_by(colors = str(colors)).all()
# 	for card in card_color:
# 		for subtype in subtypes:
# 			if subtype in card.


# --------------------------------------------------------------

# SHOWING CARDS BY MANACOST

@app.route('/manacost')
def show_card_by_manacost():

	user_input = request.get_json()
	manacost = user_input['manaCost']
	formated_manacost = ''
	cardnames = []
	for letter in manacost:
		formated_manacost += '{%s}' % letter # To get input in {letter}{letter} format
	card = Cards.query.filter_by(manaCost = formated_manacost).all()
	for number in range(len(card)):
		cardnames.append(card[number].name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY TYPES

@app.route('/types')
def show_card_by_types():

	user_input = request.get_json()
	types = user_input['types']
	cards = Cards.query.all()
	card_list = []
	for card in cards:
		for each in types:
			if each in card.types:
				card_list.append(card.name)
	print len(card_list)
	return json.dumps(dict(names = card_list))


# --------------------------------------------------------------


# SHOWING CARDS BY MANACOST AND COLOR

@app.route('/manacost/colors')
def show_card_by_mana_color():

	user_input = request.get_json()
	manacost = user_input['manaCost']
	formated_manacost = ''
	cardnames = []
	for letter in manacost:
		formated_manacost += '{%s}' % letter # To get input in {letter}{letter} format
	colors = user_input['colors']
	card_from_manacost = Cards.query.filter_by( manaCost = formated_manacost).all()
	for card in card_from_manacost:
		if card.colors == str(sorted(colors)):
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
# --------------------------------------------------------------

# SHOWING CARDS BY TEXT

@app.route('/text')
def show_card_by_text():

	user_input = request.get_json()
	text = user_input['text']
	cards = Cards.query.all()
	card_list = []
	for card in cards:
		for word in text:
			if word in card.text:
				card_list.append(card.name)
	return json.dumps(dict(names = card_list))
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
	for card in user.mycards:
		cardsnames.append(card.name)
	return json.dumps(dict(name = cardsnames))
# --------------------------------------------------------------

# SHOWING CARDS BY ARTIST

@app.route('/artist/<username>')
def show_user_card_by_artist(username):

	user_input = request.get_json()
	artist = user_input['artist']
	user = Users.query.filter_by(username = username).first()
	cardnames = []
	for card in user.mycards:
		if card.artist == artist:
			cardnames.append(card.name)
	return json.dumps(dict(names = cardnames))
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
	card_list = []
	user = Users.query.filter_by(username = username).first()
	for each in name:
		for card in user.mycards:
			if card.name == each:
				card_list.append(card)
	return str(card_list)
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

@app.route('/colors/<username>')
def show_user_card_colors(username):

  	user_input = request.get_json()
  	colors = sorted(user_input['colors'])
  	card_list = []
  	user = User.query.filter_by(user = username).first()
	for card in user.mycards:
		if card.colors == colors:
			card_list.append(card.name)
	return json.dumps(dict(names = card_list))

# --------------------------------------------------------------

# SHOWING CARDS BY TYPES

@app.route('/types/<username>')
def show_user_card_by_types(username):

	user_input = request.get_json()
	types = user_input['types']
	user = Users.query.filter_by(username = username).first()
	card_list = []
	for card in user.mycards:
		for each in types:
			if each in card.types:
				card_list.append(card.name)
	return json.dumps(dict(names = card_list))
# --------------------------------------------------------------

# SHOWING CARDS BY TEXT

@app.route('/text/<username>')
def show_user_card_by_text(username):

	user_input = request.get_json()
	text = user_input['text']
	user = Users.query.filter_by(username = username).first()
	card_list = []
	for card in user.mycards:
		for word in text:
			if word in card.text:
				card_list.append(card.name)
	return json.dumps(dict(names = card_list))
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

# DELETING USER

@app.route('/delete/<username>', methods = ['DELETE'])
def delete_user(username):

	user = Users.query.filter_by(username = username).first()
	user_id = user.user_id
	db.session.delete(user)
	db.session.commit()
	return 'User with id = %d' % user_id