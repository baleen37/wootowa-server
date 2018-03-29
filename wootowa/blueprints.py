import flask as fl


def _factory(partial_module_string, url_prefix):
    name = partial_module_string
    import_name = f'wootowa.views.{partial_module_string}'
    template_folder = 'templates'
    bp = fl.Blueprint(name, import_name, template_folder=template_folder, url_prefix=url_prefix)
    return bp


api_user_v1 = _factory('api.v1.user', '/api/v1/user')
index = _factory('index', '/')

all_blueprints = (index, api_user_v1)
