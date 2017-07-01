import enum
import uuid

from sqlalchemy import (
    Column, Integer, String, DateTime,
    Enum
)
from sqlalchemy.sql import func

from wootowa.glb.database import Base


class User(Base):
    __tablename__ = 'wootowa_users'

    class Gender(enum.Enum):
        male = 1
        female = 2

    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True)
    social_id = Column(String, nullable=False, unique=True)
    nickname = Column(String)
    gender = Column(Enum(Gender))
    age = Column(Integer)
    age2 = Column(Integer)
    age3 = Column(Integer)
    until_block_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Device(Base):
    __tablename__ = 'wootowa_devices'

    id = Column(String, nullable=False, primary_key=True)
    push_token = Column(String, nullable=True, unique=True)
    push_token2 = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime, server_default=func.now())
