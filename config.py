import os

class Config:
    DEBUG = False

    SECRET_KEY = os.environ['SECRET_KEY']
    SESSION_TYPE = os.environ['SESSION_TYPE']

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
