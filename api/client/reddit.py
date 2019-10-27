# -*- coding: utf-8 -*-
"""
    reddit
    ~~~~~~~~~
    This module contains a client to encapsulate operations against the Reddit API.
"""

from praw import Reddit
from prawcore.exceptions import ResponseException as PrawResponseException

from api.shared.constants import USER_AGENT

class RedditClientAuthenticationException(Exception):
    """ Exception given when authentication against the reddit API fails. """

    def __init__(self, message):
        self.message = message

        super().__init__()

class RedditClientException(Exception):
    """ Exception given when an action against the reddit API fails for an unexpected reason. """
    pass

class RedditClient:
    """ Encapsulates the different actions that can be performed against the reddit API. """

    def __init__(self, client_id, client_secret, token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.user_agent = USER_AGENT
        self.reddit = None
        self.authenticated = False

    def _authenticate(self):
        if self.authenticated:
            return True

        self.reddit = Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=self.token,
            user_agent=self.user_agent
        )

        try:
            user = self.reddit.user.me()

            self.authenticated = user is not None

            return self.authenticated
        except PrawResponseException:
            # This is expected if the token, client ID or client secret is not valid.
            raise RedditClientAuthenticationException('Failed to authenticate with Reddit API')
        except Exception as e:
            # This is not expected.
            raise RedditClientException(e)

    @property
    def authenticated_user(self):
        """ Returns the currently authenticated user. """
        self._authenticate()

        return self.reddit.user.me()

    def saved_posts(self, limit, subreddit=None):
        """ Returns a generator that can be used to enumerate all of a users saved posts. """

        # Attempt to authenticate first. Any exceptions must be handled by the caller.
        self._authenticate()
        user = self.reddit.user.me()

        parameters = {}

        # Filter by subreddit if requested and possible.
        if subreddit and user.has_gold_subscription:
            parameters['sr'] = subreddit

        return self.reddit.user.me().saved(limit=limit, params=parameters)
