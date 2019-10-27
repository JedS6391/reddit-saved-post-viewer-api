# -*- coding: utf-8 -*-
"""
    routes
    ~~~~~~~~~
    This module contains the main API routes.
"""

from flask import Blueprint, jsonify

api = Blueprint('api', __name__, url_prefix='/v1')

@api.route('/')
def index():
    """ Returns some basic information about the API. """
    return jsonify({
        'name:': 'Reddit Saved Post API',
        'description': 'A simple API to facilitate access to saved Reddit submissions and comments',
        'version': 1.0
    })