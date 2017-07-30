import datetime

import jwt
from glb import config
from glb.controllers.base import BaseController
from glb.storage import db_session as db

from glb.models.user import SocialUser, SocialType


class SocialController(BaseController):
    @classmethod
    def create(cls, social_type: SocialType, sub: str) -> SocialUser:
        social = SocialUser()

        assert social_type, "social_type is null"
        assert sub, "sub is null"

        social.social_id = "{}${}".format(social_type, sub)

        db.add(social)
        db.commit()

        return social

    @classmethod
    def get(cls, social_id) -> SocialUser:
        social_user = (db.query(SocialUser)
                       .filter(SocialUser.social_id == social_id)
                       .first())
        return social_user

    @staticmethod
    def encode_social_token(social_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'iat': datetime.datetime.utcnow(),
                'sub': social_id
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_social_token(auth_token):
        payload = jwt.decode(auth_token, Config.SECRET_KEY)
        return payload['sub']
