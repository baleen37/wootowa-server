import flask as fl

bp = fl.Blueprint('context_processor', __name__)


def init(app):
    app.register_blueprint(bp)


@bp.before_app_request
def block_user():
    pass
