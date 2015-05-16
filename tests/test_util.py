import pytest
from pathlib import Path

import asphalt.templating
from asphalt.templating.util import package_to_directory

BASEDIR = Path(asphalt.templating.__file__).parent


@pytest.mark.parametrize('package_path, expected', [
    ('asphalt.templating', BASEDIR),
    ('asphalt.templating/renderers', BASEDIR / 'renderers')
])
def test_package_to_directory(package_path, expected):
    assert package_to_directory(package_path) == str(expected)


@pytest.mark.parametrize('package_path, errormsg', [
    ('asphalt.templating/foobar', '{} does not exist'.format(BASEDIR / 'foobar')),
    ('asphalt.templating/api.py', '{} is not a directory'.format(BASEDIR / 'api.py'))
])
def test_package_to_directory_fail(package_path, errormsg):
    exc = pytest.raises(LookupError, package_to_directory, package_path)
    assert str(exc.value) == errormsg
