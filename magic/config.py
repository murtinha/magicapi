class BaseConfig(object):
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///storage.db'

class TestConfig (BaseConfig):
	PRESERVE_CONTEXT_ON_EXCEPTION = False
	DEBUG = True
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'