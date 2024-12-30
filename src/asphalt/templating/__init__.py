from ._api import TemplateRenderer as TemplateRenderer
from ._component import TemplatingComponent as TemplatingComponent
from ._utils import package_to_directory as package_to_directory

# Re-export imports, so they look like they live directly in this package
for __value in list(locals().values()):
    if getattr(__value, "__module__", "").startswith(f"{__name__}."):
        __value.__module__ = __name__

del __value
