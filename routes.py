from app import app,db
from jsonloadtest import data
from tables import Cards, Users
from flask import request

# HEALTH-CHECK

@app.route('/health-check')
def health_check():
	return 'It lives!!!'

@app.route('/add', methods = ['POST'])
def add_cards():
	
	# SCRIPT FOR ADDING CARDS TO THE DB
	 for cards in data['cards']:
	 	dbcreate = Cards(cards['id'],cards['name'],cards['manaCost'],str(cards['colors']),str(cards['types']),cards['rarity'],cards['text'],cards['artist'])
	 	db.session.add(dbcreate)
		db.session.commit()
	 return 'added'
	# user_input = request.get_json()
	# card_name = user_input['name']
	# card_db_filter = Cards.query.filter_by(name = card_name).first()
	# user_username = user_input['username']
	# user_email = user_input['email']
	# dbcreate = Users(user_username, user_email, card_db_filter)

	# db.session.add(dbcreate)
	# db.session.commit()

	# return 'Card name %s added' % card_db_filter.name

@app.route('/delete/<name>', methods = ['DELETE'])
def delete_card(name):
	card = Cards.query.filter_by(name = name).first()
	db.session.delete(card)
	db.session.commit()
	return '%s deleted' % name