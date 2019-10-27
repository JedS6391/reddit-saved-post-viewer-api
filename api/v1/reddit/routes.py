# -*- coding: utf-8 -*-
"""
    reddit.routes
    ~~~~~~~~~
    This module contains the main reddit API routes.
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
from api.queue.workers import SavedPostAggregator

from api.client.reddit import (
    RedditClient,
    RedditClientException,
    RedditClientAuthenticationException
)

reddit = Blueprint('reddit', __name__, url_prefix=api.url_prefix + '/reddit')

queue_service = QueueService(timeout=3600)

@reddit.route('/posts/saved/', methods=['GET'])
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

    authenticated_user = reddit_client.authenticated_user

    if not authenticated_user.has_gold_subscription and subreddit is not None:
        return jsonify({
            'error': 'subreddit filtering is only supported for gold users.'
        })

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

@reddit.route('/user/', methods=['GET'])
@token_required
def user():
    """ Gets the authenticated user details. """
    token = request.headers.get('Authorization', default=None)

    reddit_client = RedditClient(
        client_id=app.config['CLIENT_ID'],
        client_secret=app.config['CLIENT_SECRET'],
        token=token
    )

    authenticated_user = reddit_client.authenticated_user

    return jsonify({
        'id': authenticated_user.id,
        'name': authenticated_user.name,
        'has_gold_subscription': authenticated_user.has_gold_subscription,
        'created_utc': int(authenticated_user.created_utc)
    })
