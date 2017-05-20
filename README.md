An API to interact with (JSON) Magic Cards written in Python and Flask using MTGJSON data (https://mtgjson.com/)

I went a little further and crawled the image's url from ligamagic.com.br using BeautifulSoup and urllib. There are only 2 cards that the image is from another website, Verdant Automaton from mtggoldfish and Onward/Victory from wizards.

I also left all Avatar named cards without an image.

All cards are in storage DB. Besides the Cards table there are Colors,Subtypes,Types,Clans and Users table. You can create your own user and add/delete any cards you want to it. You can also add a Clan to your user, remove our update it.

All POST and PUT request have to be in JSON format.

Routes:

	- /name/ : Shows cards by name 
		(ex: /name/?name='Black Lotus')
	
	- /colors/ : Shows cards by color 
		(ex: /colors/?colors='Green,Red')
	
	- /users/ : Shows card users, everyone that has that card
	
	- /text/ : Shows cards by text 
		(ex: /text/?text='flying')
	
	- /subtypes/ : Shows cards by subtypes 
		(ex: /subtypes/?subtypes='Elf')
	
	- /colors/text/ : Shows cards by colors and text 
		(ex: /colors/text/?colors='Green'&text='Trample')
	
	- /manacost/ : Shows cards by manacost 
		(ex: /manacost/?manacost=1)
	
	- /types/ : Shows cards by types 
		(ex: /types/?types='Creature,Artifact')

	- /manacost/colors/ : Shows cards by manacost and colors 
		(ex: /manacost/colors/?manacost=1&colors='Blue')

The same routes above are equal for users, just add /<username>.
If your user is called 'Tom', then looking for cards by name would be:
	(ex: /name/tom/?name='Black Lotus' 

	- /adduser : Adds a user (username and email needed on request)
		(ex: POST username='tom' email='tom@blabla.com')

	- /addcard/<username> : Adds cards to user
		(ex: POST name= ['Black Lotus','Terror'] )

	- /cards/<username>: Shows user cards

	- /delete/<username> : Deletes user

	- /delete/card/<username> : Deletes card from user

	- /addclan/<username> : Adds clan to user
		(ex: POST clan = 'Rakdos')
	
	- /clan/<username> : Shows user clan

	- /clan/users/<clanname> : Shows clan users

	- /clan/update/<username> : Updates user clan
		(ex: PUT clan = 'Gruul')
	
