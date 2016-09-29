"""
A simple example that renders a Mako template and prints out the result.

Notice that this example specifies the template search path using  the ``directories`` option
instead of ``package_paths`` because this script is not part of a package. In practical
applications, however, it is recommended to store the templates in a directory within the
application's package tree so it can be accessed regardless of where the application has been
installed.
"""

from datetime import datetime
from pathlib import Path

from asphalt.core import CLIApplicationComponent, Context, run_application


class ApplicationComponent(CLIApplicationComponent):
    async def start(self, ctx: Context):
        this_directory = str(Path(__file__).parent)
        self.add_component('templating', backend='mako', directories=[this_directory])
        await super().start(ctx)

    async def run(self, ctx: Context):
        rendered = ctx.mako.render('demo.mako', now=datetime.now())
        print(rendered)

run_application(ApplicationComponent())
