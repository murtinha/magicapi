from flask import json

with open('AllCards.json') as json_data:
	data = json.load(json_data, strict = False)

