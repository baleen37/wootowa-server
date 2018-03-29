import tempfile

from tests.testcase import BaseTestCase
from wootowa.app import get_config, Response


class TestApp(BaseTestCase):

    def test_config_TESTING_FLAG(self):
        assert self.app.config['TESTING']

    def test_response_class_is_custom_reponse_class(self):
        assert self.app.response_class is Response


def test_get_config_yaml():
    f_path = tempfile.mktemp()
    with open(f_path, 'w') as f:
        f.write('TEST_VAR: true')

    config = get_config('wootowa.config.Testing', yaml_files=[f_path])

    assert config.TEST_VAR is True
