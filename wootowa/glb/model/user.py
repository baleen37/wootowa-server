import enum
import uuid

from sqlalchemy import (
    Column, Integer, String, DateTime,
    Enum
)
from sqlalchemy.sql import func

from wootowa.glb.model.base import Base


class User(Base):
    __tablename__ = 'users'

    class Gender(enum.Enum):
        male = 1
        female = 2

    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True)
    device_id = Column(String, nullable=False, unique=True)
    gender = Column(Enum(Gender), nullable=False)
    age = Column(Integer, nullable=False)
    until_block_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
