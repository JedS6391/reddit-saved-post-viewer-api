from flask import session
import praw

import os
import uuid

class RedditOAuthClient:

    def __init__(self):
        self.client_id = os.environ['CLIENT_ID']
        self.client_secret = os.environ['CLIENT_SECRET']
        self.redirect_uri = os.environ['REDIRECT_URI']
        self.user_agent = 'reddit-saved-post-api by /u/oracular_demon'
        # We need history scope to view saved posts.
        self.scopes = ['identity', 'history']

    @property
    def authorisation_url(self):
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
        if 'oauth_state' not in session:
            return False, None, 'no saved state in session'

        # We remove the state value from the session to prevent it being used again.
        saved_state = session.pop('oauth_state')

        if saved_state != state:
            return False, None, 'saved state does not match state being validated'

        reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            user_agent=self.user_agent
        )

        refresh_token = reddit.auth.authorize(code)
        valid = refresh_token is not None

        return valid, refresh_token, '' if valid else 'authorisation of code failed'