from app import app,db
from jsonloadtest import data
from tables import Cards

# HEALTH-CHECK

@app.route('/health-check')
def health_check():
	return 'It lives!!!'

@app.route('/add', methods = ['POST'])
def add_cards():
	for cards in data['cards']:
		dbcreate = Cards(cards['id'],cards['name'],cards['manaCost'],str(cards['colors']),str(cards['types']),cards['rarity'],cards['text'],cards['artist'])
		db.session.add(dbcreate)
		db.session.commit()
	return 'cards added'