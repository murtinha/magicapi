
def single_types(data):

	types = map(lambda card: card.get('types',''),data.values())
	types_flatten = ()

	for type in types:
		types_flatten += tuple(type)
	types_flatten = list(set(types_flatten))
	types_flatten.append("empty")


	return types_flatten

def single_subtypes(data):

	subtypes = map(lambda card: card.get('subtypes',''),data.values())
	subtypes_flatten = ()
	for subtype in subtypes:
		subtypes_flatten += tuple(subtype)
	subtypes_flatten = list(set(subtypes_flatten))
	subtypes_flatten.append("empty")
	
	return subtypes_flatten



