from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from asphalt.core import NoCurrentContext, current_context
from mako.lookup import TemplateLookup
from mako.template import Template

from asphalt.templating.api import TemplateRenderer
from asphalt.templating.utils import package_to_directory


class MakoRenderer(TemplateRenderer):
    """
    Renders Mako templates.

    .. note:: By default, the ``filesystem_checks`` argument of
      :class:`~mako.lookup.TemplateLookup` is set  to the value of the ``__debug__``
      variable. This means that in production mode, it will not check for template
      changes. If a template is edited in production mode, the application must be
      restarted for the changes to take effect.

    :param package_paths: if given, looks up the directories containing the given
        package and fills in the ``directories`` argument for
        :class:`~mako.lookup.TemplateLookup`. The value will be interpreted by
        :func:`~asphalt.templating.util.package_to_directory`.
    :param loader_args: extra arguments to pass to :class:`~mako.lookup.TemplateLookup`
    """

    __slots__ = "lookup"

    def __init__(self, package_paths: Iterable[str] = (), **lookup_options) -> None:
        directories = lookup_options.setdefault("directories", [])
        directories.extend(package_to_directory(pkg_path) for pkg_path in package_paths)
        lookup_options.setdefault("filesystem_checks", __debug__)
        self.lookup = TemplateLookup(**lookup_options)

    @staticmethod
    def _render(template: Template, vars: dict[str, Any]) -> str:
        if "ctx" not in vars:
            try:
                vars["ctx"] = current_context()
            except NoCurrentContext:
                pass

        return template.render(**vars)

    def render(self, template: str, **vars: Any) -> str:
        compiled_template = self.lookup.get_template(template)
        return self._render(compiled_template, vars)

    def render_string(self, source: str, **vars: Any) -> str:
        template = Template(source)
        return self._render(template, vars)
