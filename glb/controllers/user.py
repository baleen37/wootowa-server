import datetime

import jwt
from glb import config
from glb.storage import db_session as db

from glb.models.user import User


class UserController(object):
    def __init__(self, user: User):
        assert user, 'user is none'
        self.user = user

    @classmethod
    def create(cls, social_user_id: str, nickname: str, gender: User.Gender, age: int):
        user = User()
        user.social_user_id = social_user_id
        user.nickname = nickname
        user.gender = gender
        user.age = age

        db.add(user)
        db.commit()

        return user

    def encode_auth_token(self) -> str:
        """
        Generates the Auth Token
        :return: string
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow(),
            'sub': self.user.id
        }
        return jwt.encode(
            payload,
            config.SECRET_KEY,
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, Config.SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
