import logging
from functools import partial
from typing import Dict, Any

from asphalt.core import Component, Context, PluginContainer, merge_config, qualified_name
from typeguard import check_argument_types

from asphalt.templating.api import TemplateRenderer, TemplateRendererProxy

template_renderers = PluginContainer('asphalt.templating.renderers', TemplateRenderer)
logger = logging.getLogger(__name__)


class TemplatingComponent(Component):
    """
    Creates one or more :class:`~asphalt.templating.api.TemplateRenderer` resource factories.

    Template renderers can be configured in two ways:

    #. a single renderer, with configuration supplied directly as keyword arguments to this
        component's constructor (with the resource name being ``default`` and the context attribute
        matching the backend name)
    #. multiple renderers, by providing the ``renderers`` option where each key is the resource
        name and each value is a dictionary containing that renderer's configuration (with the
        context attribute matching the resource name by default)

    Each renderer configuration has two special options that are not passed to the constructor of
    the backend class:

    * backend: entry point name of the renderer backend class (required)
    * context_attr: name of the context attribute of the renderer resource factory

    :param renderers: a dictionary of resource name ⭢ constructor arguments for the chosen
        backend class
    :param default_renderer_args: default values for constructor keyword arguments
    """

    def __init__(self, renderers: Dict[str, Dict[str, Any]] = None, **default_renderer_args):
        assert check_argument_types()
        if not renderers:
            default_renderer_args.setdefault('context_attr', default_renderer_args.get('backend'))
            renderers = {'default': default_renderer_args}

        self.renderers = []
        for resource_name, config in renderers.items():
            config = merge_config(default_renderer_args, config or {})
            type_ = config.pop('backend', resource_name)
            context_attr = config.pop('context_attr', resource_name)
            renderer = template_renderers.create_object(type_, **config)
            self.renderers.append((resource_name, context_attr, renderer))

    async def start(self, ctx: Context):
        for resource_name, context_attr, renderer in self.renderers:
            proxymaker = partial(TemplateRendererProxy, renderer=renderer)
            types = [TemplateRenderer, type(renderer)]
            ctx.add_resource_factory(proxymaker, types, resource_name, context_attr)
            logger.info('Configured template renderer (%s / ctx.%s; class=%s)', resource_name,
                        context_attr, qualified_name(renderer))
