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

    If more than one renderer is to be configured, provide a ``renderers`` argument as a dictionary
    where the key is the resource name and the value is a dictionary of keyword arguments to
    :meth:`configure_renderer`. Otherwise, directly pass those keyword arguments to the component
    constructor itself.

    If ``renderers`` is defined, any extra keyword arguments are used as default values for
    :meth:`configure_renderer` for all renderers (:func:`~asphalt.core.util.merge_config` is used
    to merge the per-renderer arguments with the defaults). Otherwise, a single renderer is created
    based on the provided default arguments, with ``context_attr`` defaulting to the name of the
    chosen backend.

    :param renderers: a dictionary of resource name ⭢ constructor arguments for the chosen backend
        class
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
