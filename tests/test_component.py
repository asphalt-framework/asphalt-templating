import pytest
from asphalt.core import Context, add_resource, require_resource

from asphalt.templating._api import TemplateRenderer
from asphalt.templating.component import TemplatingComponent
from asphalt.templating.renderers.jinja2 import Jinja2Renderer

pytestmark = pytest.mark.anyio


async def test_single_renderer():
    async with Context():
        await add_resource("åäö")
        component = TemplatingComponent(
            backend="jinja2", options={"package_name": "tests"}
        )
        await component.start()

        for cls in (TemplateRenderer, Jinja2Renderer):
            renderer = require_resource(cls)
            assert isinstance(renderer, Jinja2Renderer)

        assert type(renderer.environment).__name__ == "Environment"
