from tests.testcase import BaseTestCase


class Test_UserAuth(BaseTestCase):
    def test_sign_up(self):
        data = {'username': 'wootowa', 'password': 'pw'}
        response = self.client.post('/api/v1/user/sign_up', data=data)

        assert response.status_code == 200
        assert response.json['data']['token']

    def test_sign_up_error(self):
        data = {'username': 'wootowa'}
        response = self.client.post('/api/v1/user/sign_up', data=data)

        assert response.status_code == 200
        assert not response.json['data']['token']
        assert response.json['message']
