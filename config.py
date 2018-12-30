# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~~~~
    This module contains the definition of configuration required by the application.
"""

import os

class Config:
    DEBUG = False

    # Secret key used across the Flask application. 
    SECRET_KEY = os.environ['SECRET_KEY']

    # Reddit API client configuration.
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
    REDIRECT_URI = os.environ['REDIRECT_URI']

    # flask-session backend configuration
    SESSION_TYPE = os.environ['SESSION_TYPE']

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
