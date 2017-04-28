from app import app,db
from jsonloadtest import data
from tables import Cards, Users
from flask import request, json

# HEALTH-CHECK

@app.route('/health-check')
def health_check():

	return 'It lives!!!'

# --------------------------------------------------------------------
# TABLE CARDS ROUTES
# --------------------------------------------------------------

# ADDING CARDS

@app.route('/add', methods = ['POST'])
def add_cards():

	for cards in data['cards']:
	 	dbcreate = Cards(cards['id'],cards['name'],cards['manaCost'],
	 		             str(cards['colors']),str(cards['types']),
	 		             cards['rarity'],cards['text'],cards['artist'])
	 	db.session.add(dbcreate)
		db.session.commit()
	return 'added'
# --------------------------------------------------------------

# SHOWING CARDS BY NAME

@app.route('/<name>')
def show_card(name):

	card = Cards.query.filter_by(name=name).first()
	return str(card)

# --------------------------------------------------------------

# DELETING CARDS

@app.route('/delete/<name>', methods = ['DELETE'])
def delete_card(name):

	card = Cards.query.filter_by(name = name).first()
	db.session.delete(card)
	db.session.commit()
	return '%s deleted' % name

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
	card = Cards.query.filter_by(name = card_name).first()
	card.owner.append(user)
	db.session.commit()
	return '%s added to %s' %(card_name,username)
# --------------------------------------------------------------

# SHOWING USER CARDS

@app.route('/cards/<username>')
def show_user_cards(username):

	user = Users.query.filter_by(username = username).first
	for cards in user.mycards:
		print cards.name
	return 'ok'
# --------------------------------------------------------------
