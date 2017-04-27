from flask import json

with open('testJSON.json') as json_data:
	data = json.load(json_data, strict = False)
