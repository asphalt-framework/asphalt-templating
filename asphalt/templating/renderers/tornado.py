from tornado.template import Loader, Template

from typeguard import check_argument_types

from asphalt.templating.api import TemplateRenderer
from asphalt.templating.util import package_to_directory


class TornadoRenderer(TemplateRenderer):
    """
    Renders Tornado templates.

    :param package_path: if given, looks up the directory containing the given package and fills in
        the ``root_directory`` argument for :class:`~tornado.template.Loader`. The value will be
        interpreted by :func:`~asphalt.templating.util.package_to_directory`.
    :param loader_args: extra arguments to pass to :class:`~tornado.template.Loader`
    """

    __slots__ = 'loader'

    def __init__(self, package_path: str = None, **loader_args):
        assert check_argument_types()
        if package_path:
            loader_args.setdefault('root_directory', package_to_directory(package_path))

        self.loader = Loader(**loader_args)

    def render(self, template: str, **vars) -> str:
        template = self.loader.load(template)
        return template.generate(**vars).decode('utf-8')

    def render_string(self, source: str, **vars) -> str:
        template = Template(source)
        return template.generate(**vars).decode('utf-8')
