from sqlalchemy.ext.declarative import declarative_base


class Model:

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Model = declarative_base(cls=Model)

from .user import *
