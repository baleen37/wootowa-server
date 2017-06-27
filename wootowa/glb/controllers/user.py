import datetime

import jwt

from wootowa.glb import config
from wootowa.glb.model.user import User
from wootowa.glb.storage import db_session as db


class UserController(object):
    @classmethod
    def get_or_create_user(cls, social_id):
        user = cls.get_user(social_id)

        if not user:
            user = User()
            user.social_id = social_id

        db.add(user)
        db.commit()

        return user

    @classmethod
    def get_user(cls, social_id=str):
        user = (db.query(User)
                .filter(User.social_id == social_id)
                .first())

        return user

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, config.SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
