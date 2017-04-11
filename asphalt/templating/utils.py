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
    pkgname, subpath = package_path.split('/', 1) if '/' in package_path else (package_path, '')
    module = import_module(pkgname)
    path = Path(module.__spec__.origin).parent / subpath
    if path.exists():
        if path.is_dir():
            return str(path)
        else:
            raise LookupError('{} is not a directory'.format(path))
    else:
        raise LookupError('{} does not exist'.format(path))
