from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from glb import config

metaData = MetaData()

print('<---- loading db_engine')
engine = create_engine(config.DATABASE_URI)
print('Done ------------------>')

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()


def init_db():
    from glb.models.user import (
        User, SocialUser, Cookie
    )
    User, SocialUser, Cookie

    Base.metadata.create_all(bind=engine)
