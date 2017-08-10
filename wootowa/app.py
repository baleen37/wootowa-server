import importlib

from flask import Flask

app = Flask(__name__)
app.config.from_object('wootowa.config')


def init_blueprint(app):
    from wootowa.apis import v1 as v1_views
    # api/v1
    for module in v1_views.__all__:
        # (package).apis.(module)을 임포트하고 init 함수를 호출
        importlib.import_module('wootowa.apis.v1.' + module, package=__name__).init(app)

    # init context processor
    from wootowa import context_processor
    context_processor.init(app)


init_blueprint(app)

from wootowa.storage import import_models
import_models()