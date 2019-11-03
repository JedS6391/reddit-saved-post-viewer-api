# -*- coding: utf-8 -*-
"""
    main
    ~~~~~~~~~
    Provides access to the main application instance.
"""

import os

from application import Application
from api.v1.routes import api as api_v1
from api.v1.auth.routes import auth as auth_v1
from api.v1.jobs.routes import jobs as jobs_v1
from api.v1.reddit.routes import reddit as reddit_v1

config = os.environ['APP_SETTINGS']
blueprints = [api_v1, auth_v1, jobs_v1, reddit_v1]

app = Application(blueprints, config)
