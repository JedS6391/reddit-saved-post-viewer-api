# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~~~~
    This module contains the definition of configuration required by the application.
"""

import os
import logging

class Config:
    """ The base configuration. """

    # Controls whether the application will run in debug mode.
    DEBUG = False

    # Secret key used across the Flask application.
    SECRET_KEY = os.environ['SECRET_KEY']

    # Reddit API client configuration.
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
    REDIRECT_URI = os.environ['REDIRECT_URI']

    # flask-session backend configuration
    SESSION_TYPE = os.environ['SESSION_TYPE']

    # Application logging level (default is DEBUG level).
    LOGGING_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    """ Production environment configuration. """
    DEBUG = False
    LOGGING_LEVEL = logging.ERROR

class DevelopmentConfig(Config):
    """ Development environment configuration. """
    DEVELOPMENT = True
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG
