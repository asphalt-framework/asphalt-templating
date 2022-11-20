from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from asphalt.core import NoCurrentContext, current_context
from django.template import Engine, Template
from django.template.context import Context

from asphalt.templating.api import TemplateRenderer
from asphalt.templating.utils import package_to_directory


class DjangoRenderer(TemplateRenderer):
    """
    Renders Django templates.

    :param engine: a Django template engine object or keyword arguments for its
        constructor
    :param package_paths: if given, looks up the directories containing the given
        package and fills in or extends the ``dirs`` argument for
        :class:`~django.template.Engine`. The value will be interpreted by
        :func:`~asphalt.templating.util.package_to_directory`.
    """

    __slots__ = "engine"

    def __init__(
        self,
        engine: Engine | dict[str, Any] = None,
        package_paths: Iterable[str] = (),
    ) -> None:
        self.engine = engine or {}  # type: Engine
        if isinstance(self.engine, dict):
            self.engine.setdefault("dirs", []).extend(
                package_to_directory(pkg) for pkg in package_paths
            )
            self.engine = Engine(**self.engine)

    @staticmethod
    def _render(template: Template, vars: dict[str, Any]) -> str:
        if "ctx" not in vars:
            try:
                vars["ctx"] = current_context()
            except NoCurrentContext:
                pass

        context = Context(vars)
        return template.render(context)

    def render(self, template: str, **vars: Any) -> str:
        compiled_template = self.engine.get_template(template)
        return self._render(compiled_template, vars)

    def render_string(self, source: str, **vars: Any) -> str:
        template = self.engine.from_string(source)
        return self._render(template, vars)
