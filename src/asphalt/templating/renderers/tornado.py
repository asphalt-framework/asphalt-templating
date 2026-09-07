from __future__ import annotations

from typing import Any

from asphalt.core import NoCurrentContext, current_context
from tornado.template import Loader, Template

from asphalt.templating.api import TemplateRenderer
from asphalt.templating.utils import package_to_directory


class TornadoRenderer(TemplateRenderer):
    """
    Renders Tornado templates.

    :param package_path: if given, looks up the directory containing the given package
        and fills in he ``root_directory`` argument for
        :class:`~tornado.template.Loader`. The value will be interpreted by
        :func:`~asphalt.templating.util.package_to_directory`.
    :param loader_args: extra arguments to pass to :class:`~tornado.template.Loader`
    """

    __slots__ = "loader"

    def __init__(self, package_path: str | None = None, **loader_args) -> None:
        if package_path:
            loader_args.setdefault("root_directory", package_to_directory(package_path))

        self.loader = Loader(**loader_args)

    @staticmethod
    def _render(template: Template, vars: dict[str, Any]) -> str:
        if "ctx" not in vars:
            try:
                vars["ctx"] = current_context()
            except NoCurrentContext:
                pass

        return template.generate(**vars).decode("utf-8")

    def render(self, template: str, **vars: Any) -> str:
        compiled_template = self.loader.load(template)
        return self._render(compiled_template, vars)

    def render_string(self, source: str, **vars: Any) -> str:
        template = Template(source)
        return self._render(template, vars)
