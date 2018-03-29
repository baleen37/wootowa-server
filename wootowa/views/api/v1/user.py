import flask as fl
from flask import jsonify

from wootowa.blueprints import api_user_v1


@api_user_v1.route('/sign_up', methods=["POST"])
def sign_up():
    username = fl.request.form.get('username')
    password = fl.request.form.get('password')

    data = {'token': 'tokensaljfkladsjflk'}
    return jsonify({
        'meta': {
            'status': 200,
            'message': 'success'
        },
        'data': data
    })
