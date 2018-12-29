# -*- coding: utf-8 -*-
"""
    application
    ~~~~~~~~~
    This module implements the central API application object.
"""

import os

from flask import Flask
from flask_session import Session

session = Session()

class Application:
    """ The main application object for the API project. """

    def __init__(self, blueprints, config, debug=True):
        self.app = Flask(__name__)
        self.blueprints = blueprints
        self.debug = debug

        self._configure_app(config)
        self._register_blueprints()

    def _register_blueprints(self):
        for blueprint in self.blueprints:
            self.app.register_blueprint(blueprint)

    def _configure_app(self, env):
        self.app.config.from_object(env)

        # Override debug config
        self.debug = self.app.config['DEBUG']

        session.init_app(self.app)

    def start_app(self):
        self.app.run(debug=self.debug)
