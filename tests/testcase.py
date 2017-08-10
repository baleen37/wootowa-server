import unittest

from wootowa.storage import db_session


class BaseTestCase(unittest.TestCase):
    pass


class ApiViewTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        db_session.drop_all()

    def tearDown(self):
        super().tearDown()
