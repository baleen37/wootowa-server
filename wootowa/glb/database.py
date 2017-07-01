from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from wootowa.glb.config import Config

metaData = MetaData()

engine = create_engine(Config.DATABASE_URI)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()


def init_db():
    from wootowa.glb.models.user import (
        User
    )
    Base.metadata.create_all(bind=engine)
