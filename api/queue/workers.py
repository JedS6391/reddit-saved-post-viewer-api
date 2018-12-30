# -*- coding: utf-8 -*-
"""
    workers
    ~~~~~~~~~
    This module contains the definition of a worker.

    Any worker sub-classes can also be part of this module.
"""

import uuid
import logging

from praw.models.reddit.submission import Submission

from api.client.reddit import (
    RedditClientAuthenticationException,
    RedditClientException
)
from api.shared.models import Post

class Worker:
    """ The base class for all workers. Implementations must override the process method. """

    def __init__(self):
        self.id = uuid.uuid4()

        logging.basicConfig()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def process(self):
        """ This method performs the actual work that this worker encapsulates. """
        raise NotImplementedError('Method must be implemented by subclass.')

class SavedPostAggregator(Worker):
    """ A worker that can process a set of saved posts from the Reddit API. """

    def __init__(self, reddit_client, limit, subreddit):
        super().__init__()

        self.reddit_client = reddit_client
        self.limit = limit
        self.subreddit = subreddit
        self.tag = '[worker-{0}]'.format(self.id)

    def process(self):
        self.logger.info(
            '%s Processing %s saved posts (subreddit=%s)',
            self.tag,
            self.limit,
            self.subreddit
        )

        try:
            saved_post_generator = self.reddit_client.saved_posts(
                self.limit,
                subreddit=self.subreddit
            )
            links = []

            # By default, posts will be sorted in the order they were saved in.
            for post in saved_post_generator:
                if isinstance(post, Submission):
                    links.append(
                        Post(post.id, post.title, post.permalink)
                    )
                else:
                    links.append(
                        Post(post.id, post.submission.title, post.permalink)
                    )

            self.logger.info('%s Processing completed', self.tag)

            return links
        except RedditClientAuthenticationException as auth_exception:
            self.logger.error('%s Failed to authenticate with reddit API', self.tag)
            self.logger.error(auth_exception)

            return None
        except RedditClientException as client_exception:
            self.logger.error(
                '%s Unexpected reddit client exception when retreiving saved posts',
                self.tag
            )
            self.logger.error(client_exception)

            return None
        except Exception as exception:
            self.logger.error('%s Unexpected exception when retreiving saved posts', self.tag)
            self.logger.error(exception)