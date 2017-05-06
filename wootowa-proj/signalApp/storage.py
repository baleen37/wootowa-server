from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from redis import BlockingConnectionPool, StrictRedis
from .session import RedisSessionInterface
from glb import config

metaData = MetaData()

session_redis_pool = BlockingConnectionPool(host=config.RABBIT_REDIS_HOST,
                                            port=config.RABBIT_REDIS_PORT,
                                            db=config.RABBIT_REDIS_DB)
engine = create_engine(config.RABBIT_DB)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

def init_session(app):
    interface = RedisSessionInterface(get_redis())
    app.session_interface = interface

def get_redis():
    return StrictRedis(connection_pool=session_redis_pool)

def init_db():
    from . import models
    models.Base.metadata.create_all(bind=engine)
