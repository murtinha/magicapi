from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.BaseConfig')
    CORS(app)
    db.init_app(app)
    return app

app = create_app()

__all__ = [ 'app', 'db' ]