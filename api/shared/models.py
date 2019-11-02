# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~~
    This module contains any object definitions that are shared through the application.
"""

class Post:
    """ Represents a saved post on Reddit. """

    def __init__(self, post_id, title, permalink, subreddit):
        self.id = post_id
        self.title = title
        self.permalink = permalink
        self.subreddit = subreddit

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Post<id: {}, title: {}, subreddit: {}>'.format(self.id, self.title, self.subreddit)
