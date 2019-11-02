# -*- coding: utf-8 -*-
"""
    tokens
    ~~~~~~~~~
    This module contains definitions for token handling/processing.
"""

from functools import wraps
from flask import jsonify, request, current_app as app

from api.client.reddit import (
    RedditClient,
    RedditClientException,
    RedditClientAuthenticationException
)

def token_required(f):
    """ Checks for the existence of a Reddit OAuth refresh token in the Authorization header. """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', default=None)

        if token is None or token == '':
            return jsonify({
                'error': 'token missing from request'
            }), 401

        # Validate that this token is legit
        try:
            reddit_client = RedditClient(
                client_id=app.config['CLIENT_ID'],
                client_secret=app.config['CLIENT_SECRET'],
                token=token
            )

            authenticated_user = reddit_client.authenticated_user
        except RedditClientAuthenticationException:
            return jsonify({
                'error': 'invalid token'
            }), 401
        except RedditClientException:
            return jsonify({
                'error': 'invalid token'
            }), 401

        return f(*args, **kwargs)

    return decorated
