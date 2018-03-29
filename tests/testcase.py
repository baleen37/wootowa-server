import unittest
from wootowa.app import create_app, get_config
from wootowa.storage import dal


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        config_obj = get_config('wootowa.config.Testing')

        cls.app = create_app(config_obj)
        dal.db_init(config_obj.SQLALCHEMY_DATABASE_URI)
        cls.client = cls.app.test_client()
