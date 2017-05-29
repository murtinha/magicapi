from flask_migrate import Migrate
from magic import *


migrate = Migrate(app,db)

from models.tables import Cards,Users, Colors, Types, Subtypes, Clans
import routes

# To initialize db, open python shell 
#from application import db -> db.create_all()

#For every change to db tables
#flask db migrate
#flask db upgrade

if __name__ == "__main__":
	app.run()