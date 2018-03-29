import hashlib, uuid
import datetime
import sqlalchemy as sa

from . import Model


class PasswordMixin:
    _encrypted_password = sa.Column(sa.String(60), nullable=False)
    _encrypted_password_salt = sa.Column(sa.String(60), nullable=False)

    @property
    def password(self):
        return self._encrypted_password

    @password.setter
    def password(self, value):
        self._encrypted_password_salt = uuid.uuid4().hex
        self._encrypted_password = hashlib.sha512(value + self._encrypted_password_salt).hexdigest()

    def check_password(self, value):
        return hashlib.sha512(value + self._encrypted_password_salt).hexdigest() == self._encrypted_password


class User(PasswordMixin, Model):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.Unicode(50), unique=True)
    nickname = sa.Column(sa.Unicode(50), nullable=False)

    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
