from wootowa.config import Testing
from wootowa.storage import dal


def test_db_init():
    dal.db_init(Testing.SQLALCHEMY_DATABASE_URI)
    assert dal.engine
    assert dal.conn_string
    assert dal.session
