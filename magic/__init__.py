from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
	app = Flask(__name__)
	app.config.from_object('magic.config.BaseConfig')
	CORS(app)
	db.init_app(app)
	return app

def create_test_app():
	app = Flask(__name__)
	app.config.from_object('magic.config.TestConfig')
	db.init_app(app)
	return app

app = create_app()