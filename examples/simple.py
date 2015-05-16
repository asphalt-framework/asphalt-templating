"""A simple example that renders a Mako template and prints out the result."""
import asyncio
from datetime import datetime
from pathlib import Path

from asphalt.core import ContainerComponent, Context, run_application


class ApplicationComponent(ContainerComponent):
    async def start(self, ctx: Context):
        this_directory = str(Path(__file__).parent)
        self.add_component('templating', backend='mako', directories=[this_directory])
        await super().start(ctx)

        result = ctx.mako.render('demo.mako', now=datetime.now())
        print(result)
        asyncio.get_event_loop().stop()

run_application(ApplicationComponent())
