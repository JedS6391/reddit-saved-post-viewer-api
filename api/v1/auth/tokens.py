# -*- coding: utf-8 -*-
"""
    tokens
    ~~~~~~~~~
    This module contains definitions for token handling/processing.
"""

from functools import wraps
from flask import jsonify, request

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
