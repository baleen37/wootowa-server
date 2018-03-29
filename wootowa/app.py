import os
from importlib import import_module

import flask as fl
import yaml
from werkzeug.utils import cached_property

from .blueprints import all_blueprints

APP_ROOT_FOLDER = os.path.dirname(__file__)


def get_config(config_class_string, yaml_files=None):
    config_module, config_class = config_class_string.rsplit('.', 1)
    config_class_object = getattr(import_module(config_module), config_class)
    config_obj = config_class_object()

    yaml_files = yaml_files or [f for f in [
        os.path.abspath(os.path.join(APP_ROOT_FOLDER, '..', 'config.yml')),
        os.path.join(APP_ROOT_FOLDER, 'config.yml')
    ] if os.path.exists(f)]

    additional_dict = dict()
    for y in yaml_files:
        with open(y) as f:
            additional_dict.update(
                yaml.load(f.read())
            )

    for key, value in additional_dict.items():
        setattr(config_obj, key, value)

    return config_obj


class Response(fl.Response):
    @cached_property
    def json(self):
        return fl.json.loads(self.data)


def create_app(config_obj):
    app = fl.Flask(__name__)
    app.config.from_object(config_obj)
    app.response_class = Response

    for bp in all_blueprints:
        import_module(bp.import_name)
        app.register_blueprint(bp)

    return app
