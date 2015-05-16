from abc import ABCMeta, abstractmethod

from asphalt.core.context import Context


class TemplateRenderer(metaclass=ABCMeta):
    """Abstract base class for template renderers."""

    __slots__ = ()

    @abstractmethod
    def render(self, template: str, **vars) -> str:
        """
        Render the named template.

        :param template: name of the template file, relative to any of the configured template
            directories
        :param vars: extra context variables made available to templates
        :return: the rendered results
        """

    @abstractmethod
    def render_string(self, template: str, **vars) -> str:
        """
        Render the template contained in the given string.

        :param template: content of the template to render
        :param vars: extra variables made available to the template
        :return: the rendered results
        """


class TemplateRendererProxy(TemplateRenderer):
    """
    Context-bound template renderer proxy.

    Adds the bound context to the variables passed to :meth:`~TemplateRenderer.render` as ``ctx``,
    unless a variable by that name was explicitly passed.

    Any variables and methods provided by the underlying renderer can be directly accessed through
    this proxy object.
    """

    __slots__ = '_ctx', '_renderer'

    def __init__(self, ctx: Context, renderer: TemplateRenderer):
        self._ctx = ctx
        self._renderer = renderer

    def __getattr__(self, name):
        return getattr(self._renderer, name)

    def render(self, template: str, **vars) -> str:
        """
        Render the named template.

        The current context will be available to the template as the ``ctx`` variable.

        :param template: name of the template file
        :param vars: extra template variables
        :return: the rendered results

        """
        vars.setdefault('ctx', self._ctx)
        return self._renderer.render(template, **vars)

    def render_string(self, source: str, **vars) -> str:
        """
        Render the template contained in the given string.

        The current context will be available to the template as the ``ctx`` variable.

        :param source: content of the template to render
        :param vars: extra variables made available to the template
        :return: the rendered results

        """
        vars.setdefault('ctx', self._ctx)
        return self._renderer.render_string(source, **vars)
