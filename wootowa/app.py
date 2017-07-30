import importlib

from flask import Flask

app = Flask(__name__)
app.config.from_object('glb.config')


def init_blueprint(app):
    from wootowa import views

    # views
    for module in views.__all__:
        # (package).views.(module)을 임포트하고 init 함수를 호출
        importlib.import_module('wootowa.views.' + module, package=__name__).init(app)

    from wootowa.views import v1 as v1_views
    # api/v1
    for module in v1_views.__all__:
        # (package).views.(module)을 임포트하고 init 함수를 호출
        importlib.import_module('wootowa.views.v1.' + module, package=__name__).init(app)

    # init context processor
    from wootowa import context_processor
    context_processor.init(app)


init_blueprint(app)
