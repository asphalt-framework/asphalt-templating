from pathlib import Path

import pytest

import asphalt.templating
from asphalt.templating._utils import package_to_directory

BASEDIR = Path(asphalt.templating.__file__).parent


@pytest.mark.parametrize(
    "package_path, expected",
    [
        ("asphalt.templating", BASEDIR),
        ("asphalt.templating/renderers", BASEDIR / "renderers"),
    ],
)
def test_package_to_directory(package_path: str, expected: Path) -> None:
    assert package_to_directory(package_path) == str(expected)


@pytest.mark.parametrize(
    "package_path, errormsg",
    [
        ("asphalt.templating/foobar", f"{BASEDIR / 'foobar'} does not exist"),
        (
            "asphalt.templating/__init__.py",
            f"{BASEDIR / '__init__.py'} is not a directory",
        ),
    ],
)
def test_package_to_directory_fail(package_path: str, errormsg: str) -> None:
    exc = pytest.raises(LookupError, package_to_directory, package_path)
    assert str(exc.value) == errormsg
