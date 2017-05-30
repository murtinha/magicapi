from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

from magic.api.cards_routes import cards_blueprint
from magic.api.users_routes import users_blueprint
from magic.api.clan_routes import clan_blueprint

def create_app():
	app = Flask(__name__)
	app.config.from_object('magic.config.BaseConfig')
	app.register_blueprint(cards_blueprint)
	app.register_blueprint(users_blueprint)
	app.register_blueprint(clan_blueprint)
	CORS(app)
	db.init_app(app)
	return app

def create_test_app():
	app = Flask(__name__)
	app.config.from_object('magic.config.TestConfig')
	app.register_blueprint(cards_blueprint)
	app.register_blueprint(users_blueprint)
	app.register_blueprint(clan_blueprint)
	db.init_app(app)
	return app

app = create_app()