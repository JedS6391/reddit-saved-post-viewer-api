# -*- coding: utf-8 -*-
"""
    jobs.routes
    ~~~~~~~~~
    This module contains the main job API routes.
"""

from flask import (
    Blueprint,
    jsonify,
    request,
    current_app as app
)

from api.v1.routes import api
from api.v1.auth.tokens import token_required
from api.queue.service import QueueService

jobs = Blueprint('jobs', __name__, url_prefix=api.url_prefix + '/jobs')

queue_service = QueueService(timeout=3600)

@jobs.route('/<id>/status/')
@token_required
def job_status(id):
    """ Provides the status of a given job. """
    status = queue_service.status(id)

    if status is None:
        return jsonify({
            'error': 'job not found.'
        })

    meta = status['meta']
    token = request.headers.get('Authorization', default=None)

    if not 'token' in meta or meta['token'] != token:
        return jsonify({
            'error': 'invalid token supplied.'
        })

    return jsonify(status)
