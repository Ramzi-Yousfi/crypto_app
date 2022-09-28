import os

class Config:
    PORT = os.environ.get('PORT') or 5000
    ENV = os.environ.get('FLASK_ENV')
    FLASK_APP = os.environ.get('APP_NAME')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class Development(Config):
    DEBUG = True
class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    DEBUG = True


class Production(Config):
    DEBUG = False
    PORT = os.environ.get('PORT') or 8080

