from flask import Flask

from wootowa.web.helpers.dynamic_blueprints import register_blueprints

app = Flask(__name__)

INSTALLED_BLUEPRINTS = [
    'web.api.v1.user'
]

register_blueprints(app, INSTALLED_BLUEPRINTS, "bp")


def run():
    app.run()
