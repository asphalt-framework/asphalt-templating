"""
A ContainerComponent demonstrating utilizing a custom loader_class
for the jinja2 backend. The jinja2 renderer is used to render the
``demo.jinja2`` template with a new unique identifier each time it
is rendered.

Any keyword arguments other than those specified by the
``Jinja2Renderer`` class  are passed directly to the ``__init__``
method of the ``loader_class``. Please see the `Jinja2 API Docs
<http://jinja.pocoo.org/docs/dev/api/#loaders>`_ for more detail.
"""

# Standard library imports
import asyncio
from pathlib import Path
from uuid import uuid1

# Local imports
from asphalt.core import ContainerComponent, Context, run_application
from jinja2 import FileSystemLoader


class ApplicationComponent(ContainerComponent):

    async def start(self, ctx: Context):
        """Add a rendering component, then render and print a document"""
        current_directory = str(Path(__file__).parent)
        # Note the arguments here will differ depending on your `loader_class`
        self.add_component('templating', backend='jinja2',
                           loader_class=FileSystemLoader,
                           searchpath=current_directory)
        await super().start(ctx)

        uuid = uuid1()
        rendered = ctx.jinja2.render('demo.jinja2', uuid=uuid)
        print(rendered)
        asyncio.get_event_loop().stop()

run_application(ApplicationComponent())
