# -*- coding: utf-8 -*-
"""
    routes
    ~~~~~~~~~
    This module contains the main API routes.
"""

from functools import wraps

from flask import Blueprint, jsonify, request

from services.client import RedditOAuthClient

api = Blueprint('api', __name__, url_prefix='/v1')

def token_required(f):
    """ Checks for the existence of a Reddit OAuth refresh token in the Authorization header. """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', default=None)

        if token is None:
            return jsonify({
                'error': 'token missing from request'
            }), 401

        return f(*args, **kwargs)

    return decorated

@api.route('/')
def index():
    return jsonify({
        'name:': 'Reddit Saved Post API',
        'description': 'A simple API to facilitate access to saved Reddit submissions and comments',
        'version': 1.0
    })

@api.route('/authorisation/generate_url/', methods=['GET'])
def login():
    """ Generates a URL that can be used to begin the OAuth flow. """

    oauth_client = RedditOAuthClient()

    return jsonify({
        'oauth_url': oauth_client.authorisation_url
    }), 200

@api.route('/authorisation/validate/', methods=['GET'])
def logout():
    """ Performs the validation portion of the OAuth flow. """

    state = request.args.get('state')
    code = request.args.get('code')

    if state is None or code is None:
        # TODO: Maybe this should be a 401 to allow the client to act upon it?
        return jsonify({
            'error': 'state or code query parameter is missing.'
        }), 400

    oauth_client = RedditOAuthClient()

    valid, token, error = oauth_client.validate(state, code)

    if not valid:
        return jsonify({
            'error': 'failed oauth validation - {0}'.format(error)
        }), 401

    return jsonify({
        'token': token
    }), 200
    
@api.route('/test/', methods=['GET'])
@token_required
def test():
    return 'Success', 200