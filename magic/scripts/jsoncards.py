from flask import json

with open('indentedcards.json') as json_data:
	data_json = json.load(json_data, strict = False)