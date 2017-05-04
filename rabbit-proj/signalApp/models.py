import hashlib
from sqlalchemy import (
    Column, Integer, String, Text, TypeDecorator, DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

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
        pw_bytes = password.encode('utf-8')
        salt_bytes = self._PASSWORD_SALT.encode('utf-8')
        return hashlib.sha256(pw_bytes + salt_bytes).hexdigest() + "," + self._PASSWORD_SALT


    def verify_password(self, candidate):
        hash_pw = self.new_password(candidate)
        return self.password == hash_pw
