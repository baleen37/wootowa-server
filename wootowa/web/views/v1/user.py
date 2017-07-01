from flask import Blueprint, request, jsonify, make_response
from wootowa.glb.controllers.user import UserController
from oauth2client import client, crypt

from wootowa.glb import config

bp = Blueprint('user', __name__, url_prefix="/api/v1/user")


@bp.route("/")
def index():
    return "user", 200


@bp.route("/authorize/google", methods=["POST"])
def oauth():
    token = request.form["token"]

    try:
        idinfo = client.verify_id_token(token,
                                        config.GOOGLE_OAUTH2_CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")

    except crypt.AppIdentityError:
        # Invalid token
        return "fail", 500
    social_id = 'google$' + idinfo['sub']

    user = UserController.get_or_create_user(social_id=social_id)
    auth_token = UserController.encode_auth_token(user.id)

    res = {
        'message': '성공',
        'data': {
            'auth_token': auth_token,
            'user_id': user.id
        }
    }
    return make_response(jsonify(res)), 200
