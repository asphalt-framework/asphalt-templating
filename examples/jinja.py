"""
A simple example that renders a Jinja2 template and prints out the result.

Notice that this example uses FileSystemLoader instead of the default PackageLoader because this
script is not part of a package. In practical applications, however, it is recommended to store
the templates in a directory within the application's package tree and use PackageLoader with the
``package_name`` option so they can be accessed regardless of where the application has been
installed.
"""

from pathlib import Path
from uuid import uuid1

from asphalt.core import CLIApplicationComponent, Context, run_application
from jinja2 import FileSystemLoader


class ApplicationComponent(CLIApplicationComponent):
    async def start(self, ctx: Context):
        this_directory = str(Path(__file__).parent)
        self.add_component('templating', backend='jinja2', loader_class=FileSystemLoader,
                           searchpath=this_directory)
        await super().start(ctx)

    async def run(self, ctx: Context):
        rendered = ctx.jinja2.render('demo.jinja2', uuid=uuid1())
        print(rendered)

run_application(ApplicationComponent())
