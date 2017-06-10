from redis import BlockingConnectionPool, StrictRedis
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from wootowa.glb import config

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


def get_redis():
    return StrictRedis(connection_pool=session_redis_pool)


def init_db():
    from wootowa.glb.model.user import User
    models.Base.metadata.create_all(bind=engine)
