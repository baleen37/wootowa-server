import flask as fl

from wootowa.helpers.api import make_api_response

bp = fl.Blueprint('main', __name__)


def init(app):
    app.register_blueprint(bp)


@bp.route('/')
def index():
    return make_api_response(
        200, msg='success')
