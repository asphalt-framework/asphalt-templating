import pytest
from asphalt.core.context import Context

from asphalt.templating.api import TemplateRenderer
from asphalt.templating.component import TemplatingComponent
from asphalt.templating.renderers.jinja2 import Jinja2Renderer


@pytest.mark.asyncio
async def test_single_renderer():
    async with Context() as ctx:
        ctx.add_resource("åäö")
        component = TemplatingComponent(
            backend="jinja2", options={"package_name": "tests"}
        )
        await component.start(ctx)

        for cls in (TemplateRenderer, Jinja2Renderer):
            renderer = ctx.require_resource(cls)
            assert isinstance(renderer, Jinja2Renderer)

        assert type(renderer.environment).__name__ == "Environment"
