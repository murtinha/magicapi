

# CARD INDEX MAPPING

{
    "mappings": {
	  "card": {
		"dynamic":"false",
		 "properties": {
			"name": {
				"type": "text"
			},
			"manaCost": {
				"type": "keyword"
			},
			"colors": {
				"type": "nested",
				"properties": {
					"colors": {
						"type": "text"
					},
					"colors_keyword": {
						"type": "keyword"
					}
				}
			},
			"types": {
				"type": "text"
			},
			"subtypes": {
				"type": "text"
			},
			"text": {
				"type": "text"
			},
			"url": {
				"type": "keyword"
			}
		}
	}
	
  }  

}
	


# INDEX

# cat testELS.json | jq -c '.[] | {"index":{}}, {name:.name,manaCost:.manaCost,url:.url,colors:.colors,types:.types,subtypes:.subtypes,text:.text}' | curl -u elastic -XPOST localhost:9200/magic/card/_bulk --data-binary @-



from flask import json
import re

with open('testELS.json', 'r') as json_data:
	data_json = json.load(json_data, strict = False)

for card in data_json.values():
	if card.get('manaCost', '') != '':
		card['manaCost'] = re.sub("\W", "",card.get('manaCost', ''))
		card['manaCost'] = sorted(card.get('manaCost'))
		card['manaCost'] = ''.join(card.get('manaCost'))
	if card.get('colors', '') != '':
		colors = sorted(card.get('colors'))
		colors_keyword = ''
		for  color in colors:
			if color == 'Blue':
				colors_keyword += 'U'
			else:
				colors_keyword += color[0]
		new_colors = []
		colors_keyword = sorted(colors_keyword)
		colors_keyword = ''.join(colors_keyword)
		new_colors.append(dict( colors = colors))
		new_colors.append(dict( colors_keyword = colors_keyword))
		card['colors'] = new_colors

with open('testELS.json','w') as data:
	new_data = json.dump(data_json, data, indent=4)


# curl -XGET 'localhost:9200/magic/card/_search?pretty' -H 'Content-Type: application/json' -d''

