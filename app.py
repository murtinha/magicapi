from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config.BaseConfig')
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from tables import Cards,Users, Colors, Types, Subtypes, Clans
import routes

# To initialize db, open python shell 
#from application import db -> db.create_all()

#For every change to db tables
#flask db migrate
#flask db upgrade
