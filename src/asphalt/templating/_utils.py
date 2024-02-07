from __future__ import annotations

from importlib import import_module
from pathlib import Path


def package_to_directory(package_path: str) -> str:
    """
    Translate a package/path specification into a real file system pathname.

    :param package_path: a package name or a package/path specification like
        ``package.subpackage/directory/subdirectory``
    :return: the translated path name
    :raises ImportError: if the package cannot be imported
    :raises LookupError: if the directory does not exist

    """
    if "/" in package_path:
        pkgname, subpath = package_path.split("/", 1)
    else:
        pkgname, subpath = package_path, ""

    module_spec = import_module(pkgname).__spec__
    if module_spec is None or module_spec.origin is None:
        raise LookupError(f"{pkgname} does not have an origin path")

    path = Path(module_spec.origin).parent / subpath
    if path.exists():
        if path.is_dir():
            return str(path)
        else:
            raise LookupError(f"{path} is not a directory")
    else:
        raise LookupError(f"{path} does not exist")
