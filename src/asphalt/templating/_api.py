from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any


class TemplateRenderer(metaclass=ABCMeta):
    """Abstract base class for template renderers."""

    __slots__ = ()

    @abstractmethod
    def render(self, template: str, **vars: Any) -> str:
        """
        Render the named template.

        :param template: name of the template file, relative to any of the configured
            template directories
        :param vars: extra context variables made available to templates
        :return: the rendered results
        """

    @abstractmethod
    def render_string(self, source: str, **vars: Any) -> str:
        """
        Render the template contained in the given string.

        :param source: content of the template to render
        :param vars: extra variables made available to the template
        :return: the rendered results
        """
