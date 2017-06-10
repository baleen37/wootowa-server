from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix="/api/v1/user")


@bp.route("/")
def index():
    return "user", 200
