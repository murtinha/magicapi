from magic import db
from magic.models.tables import Cards, Users, Colors, Types, Subtypes
from flask import request, jsonify, Blueprint, json
import re
import requests

cards_blueprint = Blueprint('cards_routes', __name__)


# HEALTH-CHECK

@cards_blueprint.route('/health-check')
def health_check():
	return 'It lives!!!'

# --------------------------------------------------------------------
# TABLE CARDS ROUTES
# --------------------------------------------------------------


@cards_blueprint.route('/')
def welcome_page():
	return 'WELCOME TO MAGICAPI'

# SHOWING CARDS BY NAME

@cards_blueprint.route('/name/', methods = ['GET'])
def show_card_by_name():

	name = request.args.get('name','')
	body = json.dumps({ "query": { "match": { "name": name}} })
	url = 'http://127.0.0.1:9200/magic/card/_search'
	headers = { 'Content-Type': 'application/json'}
	r = requests.get(url, headers = headers, data = body)
	response =  json.loads(r.text).get('hits')
	hits = response['hits'][0]
	data = hits.get('_source')
	return jsonify(data)
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR

@cards_blueprint.route('/colors/')
def show_card_colors():

  	colors = request.args.get('colors', '')
  	page = int(request.args.get('page', 1))
 	colors_list = colors.split(',')
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

@cards_blueprint.route('/users/')
def show_card_users():

	cardname = request.args.get('name','')
	users = Cards.query.filter_by( name = cardname).first()
	usernames = []
	for user in users.owner:
		usernames.append(user.username)
	return jsonify(dict(usernames = usernames))
# --------------------------------------------------------------

# SHOWING CARDS BY TEXT

@cards_blueprint.route('/text/')
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

@cards_blueprint.route('/subtypes/')
def show_card_by_subtypes():

	subtypes = request.args.get('subtypes','')
	body = { "from": 0,"size": 50, "query": { "match": { "subtypes":{ "query": subtypes, "operator":"and"}}}}
	url = 'http://127.0.0.1:9200/magic/card/_search'
	headers = { 'Content-Type': 'application/json'}
	r = requests.get(url, headers = headers, data = json.dumps(body))
	response =  json.loads(r.text).get('hits')
	total = response['total']
	hits = response['hits']
	cards = []
	for hit in hits:
		source = hit.get('_source', '')
		name = source.get('name', '')
		url = source.get('url', '')
		cards.append(dict(name = name, url = url))
	cards.append(dict(total = total))
	return jsonify(cards)
	
# --------------------------------------------------------------

# SHOWING CARDS BY COLOR,TEXT

@cards_blueprint.route('/colors/text/')
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

@cards_blueprint.route('/manacost/')
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

@cards_blueprint.route('/types/')
def show_card_by_types():

	types = request.args.get('types','')
	body = { "from": 0,"size": 50, "query": { "match": { "types":{ "query": types, "operator":"and"}}}}
	url = 'http://127.0.0.1:9200/magic/card/_search'
	headers = { 'Content-Type': 'application/json'}
	r = requests.get(url, headers = headers, data = json.dumps(body))
	response =  json.loads(r.text).get('hits')
	total = response['total']
	hits = response['hits']
	cards = []
	for hit in hits:
		source = hit.get('_source', '')
		name = source.get('name', '')
		url = source.get('url', '')
		cards.append(dict(name = name, url = url))
	cards.append(dict(total = total))
	return jsonify(cards)

# --------------------------------------------------------------


# SHOWING CARDS BY MANACOST AND COLOR

@cards_blueprint.route('/manacost/colors/')
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