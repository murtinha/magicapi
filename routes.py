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
	# for cards in data['cards']:
	# 	dbcreate = Cards(cards['id'],cards['name'],cards['manaCost'],str(cards['colors']),str(cards['types']),cards['rarity'],cards['text'],cards['artist'])
	# 	db.session.add(dbcreate)
	# 	db.session.commit()
	user_input = request.get_json()
	card_name = user_input['name']
	card_db_filter = Cards.query.filter_by(name = card_name).first()
	# card_id = card_db_filter.id
	user_username = user_input['username']
	user_email = user_input['email']
	dbcreate = Users(user_username, user_email, card_db_filter)

	db.session.add(dbcreate)
	db.session.commit()

	return card_db_filter.name