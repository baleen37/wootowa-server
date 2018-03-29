import sys

from tests.testcase import BaseTestCase


def test_python_version():
    assert 3 == sys.version_info.major
    assert 6 == sys.version_info.minor
    assert 2 == sys.version_info.micro

