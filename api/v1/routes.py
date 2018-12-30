# -*- coding: utf-8 -*-
"""
    routes
    ~~~~~~~~~
    This module contains the main API routes.
"""

from functools import wraps

from flask import (
    Blueprint,
    jsonify,
    request,
    current_app as app
)

from api.client.authentication import RedditOAuthClient
from api.client.reddit import (
    RedditClient,
    RedditClientException,
    RedditClientAuthenticationException
)
from api.queue.service import QueueService
from api.queue.workers import SavedPostAggregator

api = Blueprint('api', __name__, url_prefix='/v1')
queue_service = QueueService(timeout=3600)

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
    """ Returns some basic information about the API. """
    return jsonify({
        'name:': 'Reddit Saved Post API',
        'description': 'A simple API to facilitate access to saved Reddit submissions and comments',
        'version': 1.0
    })

@api.route('/authorisation/generate_url/', methods=['GET'])
def login():
    """ Generates a URL that can be used to begin the OAuth flow. """

    oauth_client = RedditOAuthClient(
        client_id=app.config['CLIENT_ID'],
        client_secret=app.config['CLIENT_SECRET'],
        redirect_uri=app.config['REDIRECT_URI']
    )

    return jsonify({
        'oauth_url': oauth_client.authorisation_url
    }), 200

@api.route('/authorisation/validate/', methods=['GET'])
def logout():
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

@api.route('/posts/saved/', methods=['GET'])
@token_required
def saved_posts():
    """ Initiates a job to aggregate all of the authenticated users saved posts. """

    limit = request.args.get('limit', default=None)
    subreddit = request.args.get('subreddit', default=None)
    token = request.headers.get('Authorization', default=None)

    if limit:
        # limit must be an integer
        try:
            limit = int(limit)
        except ValueError:
            return jsonify({
                'error': 'limit must be an integer.'
            })

    reddit_client = RedditClient(
        client_id=app.config['CLIENT_ID'],
        client_secret=app.config['CLIENT_SECRET'],
        token=token
    )

    try:
        worker = SavedPostAggregator(reddit_client, limit, subreddit)

        job = queue_service.enqueue(worker)

        return jsonify({
            'job_id': job.id
        })
    except RedditClientAuthenticationException as auth_exception:
        app.logger.error('Failed to authenticate with reddit API')
        app.logger.error(auth_exception)
    except RedditClientException as client_exception:
        app.logger.error('Unexpected reddit client exception when retreiving saved posts')
        app.logger.error(client_exception)

# TODO: Should this require reddit authentication to access?
# TODO: Should this be on a per-worker basis? (i.e. different endpoints for different workers)
@api.route('/jobs/<id>/status/')
def job_status(id):
    """ Provides the status of a given job. """
    status = queue_service.status(id)

    return jsonify({
        'status': status
    })
