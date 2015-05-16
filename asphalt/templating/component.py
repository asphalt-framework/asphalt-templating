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
    Publishes one or more :class:`~asphalt.templating.api.TemplateRenderer` lazy resources.

    If more than one renderer is to be configured, provide a ``renderers`` argument as a dictionary
    where the key is the resource name and the value is a dictionary of keyword arguments to
    :meth:`configure_renderer`. Otherwise, directly pass those keyword arguments to the component
    constructor itself.

    If ``renderers`` is defined, any extra keyword arguments are used as default values for
    :meth:`configure_renderer` for all renderers (:func:`~asphalt.core.util.merge_config` is used
    to merge the per-renderer arguments with the defaults). Otherwise, a single renderer is created
    based on the provided default arguments, with ``context_attr`` defaulting to the name of the
    chosen backend.

    :param renderers: a dictionary of resource name ⭢ :meth:`configure_renderer` keyword arguments
    :param default_renderer_args: default values for :meth:`configure_renderer`
    """

    def __init__(self, renderers: Dict[str, Dict[str, Any]] = None, **default_renderer_args):
        assert check_argument_types()
        renderers = renderers or {}
        if default_renderer_args:
            default_renderer_args.setdefault('context_attr', default_renderer_args.get('backend'))
            renderers['default'] = default_renderer_args

        self.renderers = []
        for resource_name, config in renderers.items():
            config = merge_config(default_renderer_args, config)
            config.setdefault('backend', resource_name)
            config.setdefault('context_attr', resource_name)
            context_attr, renderer = self.configure_renderer(**config)
            self.renderers.append((resource_name, context_attr, renderer))

    @classmethod
    def configure_renderer(cls, context_attr: str, backend: str, **backend_args):
        """
        Configure a template renderer.

        :param context_attr: context attribute of the renderer (if omitted, the resource name
            will be used instead)
        :param backend: entry point name used to look up the backend class (if omitted, the
            resource name will be used instead)
        :param backend_args: keyword arguments passed to the constructor of the backend class

        """
        assert check_argument_types()
        renderer = template_renderers.create_object(backend, **backend_args)
        return context_attr, renderer

    async def start(self, ctx: Context):
        for resource_name, context_attr, renderer in self.renderers:
            proxymaker = partial(TemplateRendererProxy, renderer=renderer)
            ctx.publish_lazy_resource(proxymaker, TemplateRenderer, resource_name, context_attr)
            logger.info('Configured template renderer (%s / ctx.%s; class=%s)', resource_name,
                        context_attr, qualified_name(renderer))
