from typing import Any, Dict, Iterable, Union

from django.template import Engine
from django.template.context import Context
from typeguard import check_argument_types

from asphalt.templating.api import TemplateRenderer
from asphalt.templating.utils import package_to_directory


class DjangoRenderer(TemplateRenderer):
    """
    Renders Django templates.

    :param engine: a Django template engine object or keyword arguments for its constructor
    :param package_paths: if given, looks up the directories containing the given package and fills
        in or extends the ``dirs`` argument for :class:`~django.template.Engine`. The value will be
        interpreted by :func:`~asphalt.templating.util.package_to_directory`.
    """

    __slots__ = 'engine'

    def __init__(self, engine: Union[Engine, Dict[str, Any]] = None,
                 package_paths: Iterable[str] = ()) -> None:
        assert check_argument_types()
        self.engine = engine or {}  # type: Engine
        if isinstance(self.engine, dict):
            self.engine.setdefault('dirs', []).extend(package_to_directory(pkg) for
                                                      pkg in package_paths)
            self.engine = Engine(**self.engine)

    def render(self, template: str, **vars) -> str:
        compiled_template = self.engine.get_template(template)
        context = Context(vars)
        return compiled_template.render(context)

    def render_string(self, source: str, **vars) -> str:
        template = self.engine.from_string(source)
        context = Context(vars)
        return template.render(context)
