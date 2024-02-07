from typing import Any

from ._api import TemplateRenderer as TemplateRenderer
from ._utils import package_to_directory as package_to_directory

# Re-export imports, so they look like they live directly in this package
key: str
value: Any
for key, value in list(locals().items()):
    if getattr(value, "__module__", "").startswith("asphalt.templating."):
        value.__module__ = __name__
