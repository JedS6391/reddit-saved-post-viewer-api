# -*- coding: utf-8 -*-
"""
    authentication
    ~~~~~~~~~
    This module contains any logic relating to the Reddit OAuth flow.
"""

import uuid

from flask import session
import praw

from api.shared.constants import USER_AGENT

# We need history scope to view saved posts.
REDDIT_AUTH_SCOPES = [
    'identity',
    'history',
    'read',
    'mysubreddits'
]

class RedditOAuthValidateResponse:
    """ Represents the status of the validation part of the OAuth flow. """

    def __init__(self, valid, token, error):
        self.valid = valid
        self.token = token
        self.error = error

class RedditOAuthClient:
    """ Handles the OAuth flow against the reddit API. """

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.user_agent = USER_AGENT
        self.scopes = REDDIT_AUTH_SCOPES

    @property
    def authorisation_url(self):
        """ Generates a URL that can be used to start the OAuth flow. """

        reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            user_agent=self.user_agent
        )

        state = str(uuid.uuid4())

        # Save the state parameter so we can validate it during the verification flow.
        session['oauth_state'] = state

        return reddit.auth.url(self.scopes, state=state, duration='permanent')

    def validate(self, state, code):
        """ Performs the validation step of the OAuth flow. """

        if 'oauth_state' not in session:
            return RedditOAuthValidateResponse(
                valid=False,
                token=None,
                error='No saved state in session'
            )

        # We remove the state value from the session to prevent it being used again.
        saved_state = session.pop('oauth_state')

        if saved_state != state:
            return RedditOAuthValidateResponse(
                valid=False,
                token=None,
                error='Saved state does not match state being validated'
            )

        reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            user_agent=self.user_agent
        )

        refresh_token = reddit.auth.authorize(code)
        valid = refresh_token is not None

        return RedditOAuthValidateResponse(
            valid=valid,
            token=refresh_token,
            error='' if valid else 'Authorisation of code failed'
        )
