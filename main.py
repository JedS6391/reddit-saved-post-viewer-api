import os

from application import Application
from api.v1.routes import api as api_v1

config = os.environ['APP_SETTINGS']
blueprints = [api_v1]

app = Application(blueprints, config, debug=True)
