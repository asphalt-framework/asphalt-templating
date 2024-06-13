from __future__ import annotations

import logging
from dataclasses import InitVar, dataclass, field
from typing import Any

from asphalt.core import (
    Component,
    PluginContainer,
    add_resource,
    qualified_name,
)

from ._api import TemplateRenderer

template_renderers = PluginContainer("asphalt.templating.renderers", TemplateRenderer)
logger = logging.getLogger(__name__)


@dataclass
class TemplatingComponent(Component):
    """
    Creates a template renderer resource.

    The renderer resource will be available in the context as the following types:

    * :class:`~asphalt.templating.TemplateRenderer`
    * its actual type

    :param backend: the name of the renderer backend
    :param resource_name: the name of the renderer resource
    :param options: a dictionary of keyword arguments passed to the template renderer
        backend class
    """

    backend: InitVar[str]
    options: InitVar[dict[str, Any] | None]
    resource_name: str = "default"
    renderer: TemplateRenderer = field(init=False)

    def __post_init__(
        self, backend: str, options: dict[str, Any] | None = None
    ) -> None:
        self.renderer = template_renderers.create_object(backend, **options or {})

    async def start(self) -> None:
        types: list[type[TemplateRenderer]] = [TemplateRenderer, type(self.renderer)]  # type: ignore[type-abstract]
        add_resource(self.renderer, self.resource_name, types=types)
        logger.info(
            "Configured template renderer (%s; class=%s)",
            self.resource_name,
            qualified_name(self.renderer),
        )
