from __future__ import annotations

import logging
from typing import Any

from asphalt.core import Component, Context, PluginContainer, qualified_name

from asphalt.templating.api import TemplateRenderer

template_renderers = PluginContainer("asphalt.templating.renderers", TemplateRenderer)
logger = logging.getLogger(__name__)


class TemplatingComponent(Component):
    """
    Creates a template renderer resource.

    The renderer resource will be available in the context as the following types:

    * :class:`~asphalt.templating.api.TemplateRenderer`
    * its actual type

    :param backend: the name of the renderer backend
    :param resource_name: the name of the renderer resource
    :param options: a dictionary of keyword arguments passed to the template renderer
        backend class
    """

    def __init__(
        self,
        backend: str,
        resource_name: str = "default",
        options: dict[str, Any] | None = None,
    ):
        options = options or {}
        self.resource_name = resource_name
        self.renderer = template_renderers.create_object(backend, **options)

    async def start(self, ctx: Context):
        types = [TemplateRenderer, type(self.renderer)]
        ctx.add_resource(self.renderer, self.resource_name, types=types)
        logger.info(
            "Configured template renderer (%s; class=%s)",
            self.resource_name,
            qualified_name(self.renderer),
        )
