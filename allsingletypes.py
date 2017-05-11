from loadjsoncards import data

types = map(lambda card: card.get('types',''),data.values())
subtypes = map(lambda card: card.get('subtypes',''),data.values())
types_flatten = ()
subtypes_flatten = ()

for type in types:
	types_flatten += tuple(type)
types_flatten = list(set(types_flatten))
types_flatten.append("empty")

for subtype in subtypes:
	subtypes_flatten += tuple(subtype)
subtypes_flatten = list(set(subtypes_flatten))
subtypes_flatten.append("empty")



