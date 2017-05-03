from sqlalchemy import Table, MetaData
from .. import config

metaData = MetaData()

engine = create_engine(config.RABBIT_DB)
