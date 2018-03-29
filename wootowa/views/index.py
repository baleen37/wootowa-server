import flask as fl
from ..blueprints import index


@index.route('/')
def main():
    return fl.redirect(fl.url_for('api.v1.user.sign_up'))
