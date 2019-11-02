# -*- coding: utf-8 -*-
"""
    application
    ~~~~~~~~~
    This module implements the central API application object.
"""

from flask import Flask
from flask_session import Session
from flask_cors import CORS

from api.shared.encoders import PostEncoder

session = Session()
cors = CORS(supports_credentials=True)

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
        cors.init_app(self.app)

        # Custom JSON encoder that can handle reddit post instances.
        self.app.json_encoder = PostEncoder

    def start_app(self):
        self.app.run(debug=self.debug)
