from flask import Blueprint

bp = Blueprint('api.v1.user', __name__, url_prefix="/api/v1/user")


def init(app):
    app.register_blueprint(bp)
