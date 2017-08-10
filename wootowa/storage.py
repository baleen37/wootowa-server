from wootowa.models.base import Base
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from wootowa import config
from wootowa.utils import sysutil

metaData = MetaData()

print('<---- loading db_engine')
if sysutil.is_unittest():
    print('------- unit test engine -----')

    engine = create_engine("sqlite:///memory")
else:
    engine = create_engine(config.DATABASE_URI)
print('Done ------------------>')

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)


def init_db():
    import_models()
    Base.metadata.create_all(bind=engine)


def drop_db():
    import_models()
    Base.metadata.drop_all(bind=engine)


def import_models():
    from wootowa import models
    print(f'import_models {models}')
