# -*- coding: utf-8 -*-
"""
    application
    ~~~~~~~~~
    This module implements the central API application object.
"""

import logging

from flask import Flask
from flask_session import Session
from flask_cors import CORS

from api.shared.encoders import PostEncoder

session = Session()
cors = CORS(supports_credentials=True)

class Application:
    """ The main application object for the API project. """

    def __init__(self, blueprints, config):
        self.app = Flask(__name__)
        self.blueprints = blueprints
        self.debug = False
        self.logger = logging.getLogger(__name__)

        self._configure_app(config)
        self._register_blueprints()

    def _register_blueprints(self):
        for blueprint in self.blueprints:
            self.app.register_blueprint(blueprint)

    def _configure_app(self, env):
        self.app.config.from_object(env)

        # Configure logging as the first step.
        logging.basicConfig(level=self.app.config['LOGGING_LEVEL'])

        self.logger.debug('Configuring application...')

        # Override debug config
        self.debug = self.app.config['DEBUG']

        if self.debug:
            self.logger.debug('Configuration: %s', self.app.config)

        session.init_app(self.app)
        cors.init_app(self.app)

        # Custom JSON encoder that can handle reddit post instances.
        self.app.json_encoder = PostEncoder

        self.logger.debug('Application configured.')

    def start_app(self):
        """ Starts the application. """
        self.logger.debug('Starting application...')

        self.app.run(debug=self.debug)
