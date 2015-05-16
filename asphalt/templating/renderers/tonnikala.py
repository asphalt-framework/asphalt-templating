from typing import Iterable

from tonnikala import FileLoader

from asphalt.templating.api import TemplateRenderer
from asphalt.templating.util import package_to_directory


class TonnikalaRenderer(TemplateRenderer):
    """
    Renders Tonnikala templates.

    :param package_paths: if given, looks up the directories containing the given package and fills
        in the ``paths`` argument for :class:`~tonnikala.FileLoader`. The value will be
        interpreted by :func:`~asphalt.templating.util.package_to_directory`.
    :param loader_args: extra arguments to pass to :class:`~tonnikala.FileLoader`
    """

    __slots__ = 'loader'

    def __init__(self, package_paths: Iterable[str] = (), **loader_args):
        paths = loader_args.setdefault('paths', [])
        paths.extend(package_to_directory(pkg_path) for pkg_path in package_paths)
        self.loader = FileLoader(**loader_args)

    def render(self, template: str, **vars) -> str:
        template = self.loader.load(template)
        return template.render(vars)

    def render_string(self, source: str, **vars) -> str:
        template = self.loader.load_string(source)
        return template.render(vars)
