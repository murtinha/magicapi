from flask_migrate import Migrate
from magic import app,db

migrate = Migrate(app,db)

from magic.models.tables import Cards,Users, Colors, Types, Subtypes, Clans

# To initialize db, open python shell 
#from application import db -> db.create_all()

#For every change to db tables
#flask db migrate
#flask db upgrade

if __name__ == "__main__":
	app.run(host='0.0.0.0')