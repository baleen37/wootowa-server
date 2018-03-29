from tests.testcase import BaseTestCase


class TestIndex(BaseTestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
