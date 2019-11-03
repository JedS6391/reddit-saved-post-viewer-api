# -*- coding: utf-8 -*-
"""
    encoders
    ~~~~~~~~~
    This module contains custom encoders for the application.
"""

from flask.json import JSONEncoder

from api.shared.models import Post

class PostEncoder(JSONEncoder):
    """ A custom `JSONEncoder` implementation that can handle `Post` objects. """

    def default(self, o):
        if isinstance(o, Post):
            return {
                'id': o.id,
                'title': o.title,
                'permalink': o.permalink,
                'subreddit': o.subreddit
            }
        return super(PostEncoder, self).default(o)