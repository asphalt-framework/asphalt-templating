from __future__ import annotations

import pytest
from asphalt.core import Context, add_resource, get_resource_nowait

from asphalt.templating import TemplateRenderer, TemplatingComponent
from asphalt.templating.renderers.jinja2 import Jinja2Renderer

pytestmark = pytest.mark.anyio


async def test_single_renderer() -> None:
    async with Context():
        add_resource("åäö")
        component = TemplatingComponent(
            backend="jinja2", options={"package_name": "tests"}
        )
        await component.start()

        renderer = get_resource_nowait(TemplateRenderer)  # type: ignore[type-abstract]
        assert isinstance(renderer, Jinja2Renderer)

        renderer = get_resource_nowait(Jinja2Renderer)
        assert isinstance(renderer, Jinja2Renderer)

        assert type(renderer.environment).__name__ == "Environment"
