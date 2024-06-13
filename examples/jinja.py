"""
A simple example that renders a Jinja2 template and prints out the result.

Notice that this example uses FileSystemLoader instead of the default PackageLoader
because this script is not part of a package. In practical applications, however, it is
recommended to store the templates in a directory within the application's package tree
and use PackageLoader with the ``package_name`` option so they can be accessed
regardless of where the application has been installed.
"""

from pathlib import Path
from uuid import uuid1

from asphalt.core import (
    CLIApplicationComponent,
    get_resource_nowait,
    run_application,
)
from jinja2 import FileSystemLoader

from asphalt.templating import TemplateRenderer


class ApplicationComponent(CLIApplicationComponent):
    async def start(self) -> None:
        this_directory = str(Path(__file__).parent)
        self.add_component(
            "templating",
            backend="jinja2",
            options={
                "loader_class": FileSystemLoader,
                "searchpath": this_directory,
            },
        )

    async def run(self) -> None:
        renderer = get_resource_nowait(TemplateRenderer)  # type: ignore[type-abstract]
        rendered = renderer.render("demo.jinja2", uuid=uuid1())
        print(rendered)


run_application(ApplicationComponent)
