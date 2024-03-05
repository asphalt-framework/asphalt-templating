from typing import Any

from ._api import TemplateRenderer as TemplateRenderer
from ._component import TemplatingComponent as TemplatingComponent
from ._utils import package_to_directory as package_to_directory

# Re-export imports, so they look like they live directly in this package
key: str
value: Any
for key, value in list(locals().items()):
    if getattr(value, "__module__", "").startswith(f"{__name__}."):
        value.__module__ = __name__
