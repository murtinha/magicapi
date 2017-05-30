from magic import db
from magic.models.tables import Cards, Users, Clans
from flask import request, jsonify, Blueprint

clan_blueprint = Blueprint('clan_routes', __name__)

# --------------------------------------------------------------
# TABLE CLANS ROUTES
# --------------------------------------------------------------

# ADDING USER TO CLAN

@clan_blueprint.route('/addclan/<username>', methods = ['POST'])
def add_user_to_clan(username):

	user_input = request.get_json()
	userclan = user_input['clan']
	user = Users.query.filter_by(username = username).first()
	if user.myclan == None:
	 	clan_ref = Clans.query.filter_by(clan_name = userclan).first()
	 	clan_ref.user_ref.append(user)
		db.session.commit()
	else:
		my_clan = Clans.query.filter_by(clan_id = user.my_clan).first()
		return 'You already have a clan (%s)!' % my_clan.clan_name
	return 'Clan %s added to User %s' % (clan_ref.clan_name, user.username)
# --------------------------------------------------------------

# SHOWING USER CLAN

@clan_blueprint.route('/clan/<username>')
def show_user_clan(username):

	user = Users.query.filter_by(username = username).first()
	clan_id = user.my_clan
	clan = Clans.query.filter_by(clan_id = clan_id).first()

	return 'Your clan is %s' % clan.clan_name
# --------------------------------------------------------------

# SHOWING CLAN USERS

@clan_blueprint.route('/clan/users/<clanname>')
def show_clan_users(clanname):

	clan = Clans.query.filter_by(clan_name = clanname).first()
	clan_id = clan.clan_id
	users = Users.query.filter_by(my_clan = clan_id).all()
	user_names = []
	for user in users:
		user_names.append(user.username)
	return jsonify(dict(users = user_names))
# --------------------------------------------------------------

# UPDATING USER CLAN

@clan_blueprint.route('/clan/update/<username>', methods = ['PUT'])
def update_clan_users(username):

	user_input = request.get_json()
	clan = user_input['clan']
	user = Users.query.filter_by(username = username).first()
	old_clan = Clans.query.filter_by(clan_id = user.my_clan).first()
	old_clan_name = old_clan.clan_name 
	new_clan = Clans.query.filter_by(clan_name = clan).first()
	new_clan.user_ref.append(user)
	db.session.commit()
	return 'You changed from %s to %s' % (old_clan_name,clan)
# --------------------------------------------------------------