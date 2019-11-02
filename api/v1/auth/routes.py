# -*- coding: utf-8 -*-
"""
    auth.routes
    ~~~~~~~~~
    This module contains the main authentication/authorisation API routes.
"""

from flask import (
    Blueprint,
    jsonify,
    request,
    current_app as app
)

from api.v1.routes import api
from api.client.authentication import RedditOAuthClient

auth = Blueprint('auth', __name__, url_prefix=api.url_prefix + '/auth')

@auth.route('/generate_url/', methods=['GET'])
def generate_url():
    """ Generates a URL that can be used to begin the OAuth flow. """

    oauth_client = RedditOAuthClient(
        client_id=app.config['CLIENT_ID'],
        client_secret=app.config['CLIENT_SECRET'],
        redirect_uri=app.config['REDIRECT_URI']
    )

    return jsonify({
        'url': oauth_client.authorisation_url
    }), 200

@auth.route('/validate/', methods=['GET'])
def validate():
    """ Performs the validation portion of the OAuth flow. """

    state = request.args.get('state', default=None)
    code = request.args.get('code', default=None)

    if state is None or code is None:
        # TODO: Maybe this should be a 401 to allow the client to act upon it?
        return jsonify({
            'error': 'state or code query parameter is missing.'
        }), 400

    oauth_client = RedditOAuthClient(
        client_id=app.config['CLIENT_ID'],
        client_secret=app.config['CLIENT_SECRET'],
        redirect_uri=app.config['REDIRECT_URI']
    )

    validation_response = oauth_client.validate(state, code)

    if not validation_response.valid:
        return jsonify({
            'error': 'failed oauth validation - {0}'.format(validation_response.error)
        }), 401

    return jsonify({
        'token': validation_response.token
    }), 200
    