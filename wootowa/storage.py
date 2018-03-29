import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, scoped_session


class DataAccessLayer:
    engine = None
    conn_string = None
    session = None
    metadata = MetaData()

    def db_init(self, conn_string):
        self.engine = sa.create_engine(conn_string)
        self.metadata.create_all(self.engine)
        self.conn_string = conn_string
        self.session = scoped_session(sessionmaker(bind=self.engine))


dal = DataAccessLayer()
