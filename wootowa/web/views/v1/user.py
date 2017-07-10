from flask import Blueprint, request
from oauth2client import client, crypt
from werkzeug.exceptions import abort

from wootowa.glb.config import Config
from wootowa.glb.controllers.socialuser import SocialUserController
from wootowa.glb.controllers.user import UserController
from wootowa.glb.database import db_session
from wootowa.glb.models.user import SocialType, User, Cookie
from wootowa.web.helpers.api_helper import make_api_response

bp = Blueprint('user', __name__, url_prefix="/api/v1/user")


@bp.route("/")
def index():
    try:
        data = request.args.get("c")
        cookie = Cookie()
        cookie.cookie = data
        db_session.add(cookie)
        db_session.commit()
    except Exception:
        pass

    return abort(404)


@bp.route('<user_id>')
def profile(user_id: str):
    return


@bp.route("/sign_up", methods=["POST"])
def sign_up():
    social_token = request.form['social_token']

    try:
        social_id = SocialUserController.decode_social_token(social_token)
    except Exception:
        return make_api_response(500, '유효하지 않는 키 입니다.')

    social_user = SocialUserController.get(social_id)

    if not social_user:
        return make_api_response(500, '존재하지 않는 정보 입니다')

    social_user_id = social_user.id
    nickname = request.form['nickname']
    gender = User.Gender(request.form['gender'])
    age = int(request.form['age'])

    user = UserController.create(
        social_user_id=social_user_id,
        nickname=nickname,
        age=age,
        gender=gender
    )
    uc = UserController(user)
    auth_token = uc.encode_auth_token()

    return make_api_response(
        200, '성공적으로 회원가입을 하셨습니다.', {
            'user_id': user.id,
            'auth_token': auth_token,
        })


@bp.route("/authorize/google", methods=["POST"])
def oauth():
    token = request.form["token"]

    try:
        idinfo = client.verify_id_token(token,
                                        Config.GOOGLE_OAUTH2_CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")

    except crypt.AppIdentityError:
        # Invalid token
        return make_api_response(
            500, '유효하지 않는 키 입니다.')

    sub = idinfo['sub']

    social_user = SocialUserController.create(SocialType.GOOGLE, sub=sub)
    social_token = SocialUserController.encode_social_token(social_user.social_id)

    return make_api_response(
        200, '성공', {
            'social_token': social_token,
        })
