# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~~
    This module contains any object definitions that are shared through the application.
"""

class Post:
    """ Represents a saved post on Reddit. """

    def __init__(self, post_id, title, permalink):
        self.id = post_id
        self.title = title
        self.permalink = permalink
