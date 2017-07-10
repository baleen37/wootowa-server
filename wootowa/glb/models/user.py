import enum
import uuid

import sqlalchemy  as sa
from sqlalchemy.sql import func

from wootowa.glb.database import Base


class SocialUser(Base):
    __tablename__ = 'wootowa_socials'

    id = sa.Column(sa.Integer, primary_key=True)
    social_id = sa.Column(sa.String, nullable=False, unique=True)
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return 'SocialUser <id {}, social_id {}>'.format(self.id, self.social_id)


class SocialType(enum.Enum):
    GOOGLE = 'google'


class User(Base):
    __tablename__ = 'wootowa_users'

    class Gender(enum.Enum):
        male = "M"
        female = "F"

    id = sa.Column(sa.String, default=lambda: str(uuid.uuid4()), primary_key=True)
    social_user_id = sa.Column(sa.Integer, sa.ForeignKey(SocialUser.id), nullable=False, unique=True)
    nickname = sa.Column(sa.String, nullable=False)
    gender = sa.Column(sa.Enum(Gender), nullable=False)
    age = sa.Column(sa.Integer, nullable=False)
    until_block_at = sa.Column(sa.DateTime, nullable=True)
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return 'User <id {}, nickname {}>'.format(self.id, self.nickname)


class Cookie(Base):
    __tablename__ = 'wootowa_cookies'

    id = sa.Column(sa.Integer, primary_key=True)
    cookie = sa.Column(sa.String, nullable=False, unique=True)
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=func.now())
