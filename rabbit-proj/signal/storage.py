from sqlalchemy import Table, MetaData, create_engine
from redis import BlockingConnectionPool, StrictRedis
from .session import RedisSessionInterface
from glb import config

metaData = MetaData()

redis_pool = BlockingConnectionPool(host=config.RABBIT_REDIS_HOST,
                                    port=config.RABBIT_REDIS_PORT,
                                    db=config.RABBIT_REDIS_DB)

def init_engine(config):
    global engine
    engine = create_engine(config)
    return engine

def init_session(app):
    interface = RedisSessionInterface(redis_pool)
    app.session_interface = interface

def get_redis():
    return StrictRedis(connection_pool=redis_pool)
