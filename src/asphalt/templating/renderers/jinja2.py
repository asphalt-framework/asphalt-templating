from __future__ import annotations

from typing import Any, Dict, Union

from asphalt.core import resolve_reference
from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from typeguard import check_argument_types

from asphalt.templating.api import TemplateRenderer


class Jinja2Renderer(TemplateRenderer):
    """
    Renders Jinja2 templates.

    A new template loader will be created if no environment is supplied or it does not already have
    a loader in it.

    .. seealso:: `Jinja2 API Docs <http://jinja.pocoo.org/docs/dev/api/#loaders>`_

    :param environment: a Jinja2 environment object or keyword arguments for its constructor
    :param loader_class: a Jinja2 template loader class or a ``module:varname`` reference to one
    :param loader_args: extra arguments to pass to the loader class
    """

    __slots__ = 'environment'

    def __init__(self, environment: Union[Environment, Dict[str, Any]] = None,
                 loader_class: Union[type, str] = PackageLoader, **loader_args) -> None:
        assert check_argument_types()
        if environment is None:
            environment = {}
        if isinstance(environment, dict):
            environment = Environment(**environment)
        self.environment = environment

        if self.environment.loader is None:
            resolved_loader_class = resolve_reference(loader_class)
            self.environment.loader = resolved_loader_class(**loader_args)

    def render(self, template: str, **vars) -> str:
        compiled_template = self.environment.get_template(template)
        return compiled_template.render(vars)

    def render_string(self, source: str, **vars) -> str:
        template = self.environment.from_string(source)
        return template.render(vars)
