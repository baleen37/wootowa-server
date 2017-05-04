import hashlib
import jwt
import datetime
from sqlalchemy import (
    Column, Integer, String, Text, TypeDecorator, DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from glb import config

Base = declarative_base()

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    _PASSWORD_SALT = 'd41d8cd98f00b204e9800998ecf8427e'

    @classmethod
    def new_password(self, password):
        '''
        Generates the password hash
        '''
        pw_bytes = password.encode('utf-8')
        salt_bytes = self._PASSWORD_SALT.encode('utf-8')
        return hashlib.sha256(pw_bytes + salt_bytes).hexdigest() + "," + self._PASSWORD_SALT


    def verify_password(self, candidate):
        '''
        Verify password hash
        '''
        hash_pw = self.new_password(candidate)
        return self.password == hash_pw

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=90, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
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
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, config.SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError as e:
            return e
        except jwt.InvalidTokenError as e:
            return e

