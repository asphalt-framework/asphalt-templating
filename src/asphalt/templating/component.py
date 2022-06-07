from __future__ import annotations

import logging
from functools import partial
from typing import Any

from asphalt.core import Component, Context, PluginContainer, qualified_name

from asphalt.templating.api import TemplateRenderer, TemplateRendererProxy

template_renderers = PluginContainer("asphalt.templating.renderers", TemplateRenderer)
logger = logging.getLogger(__name__)


class TemplatingComponent(Component):
    """
    Creates a template renderer resource factory.

    The template renderer resources will be available in the context as
     :class:`~asphalt.templating.api.TemplateRenderer` resources.

    :param backend: the name of the renderer backend
    :param resource_name: the name of the renderer resource factory
    :param options: a dictionary of keyword arguments passed to the renderer backend
        class
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
        proxymaker = partial(TemplateRendererProxy, renderer=self.renderer)
        types = [TemplateRenderer, type(self.renderer)]
        ctx.add_resource_factory(proxymaker, types, self.resource_name)
        logger.info(
            "Configured template renderer (%s; class=%s)",
            self.resource_name,
            qualified_name(self.renderer),
        )
