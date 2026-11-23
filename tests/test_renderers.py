from pathlib import Path
from typing import cast

import pytest
from asphalt.core import Context
from pytest import FixtureRequest

from asphalt.templating.api import TemplateRenderer
from asphalt.templating.renderers.django import DjangoRenderer
from asphalt.templating.renderers.jinja2 import Jinja2Renderer
from asphalt.templating.renderers.mako import MakoRenderer
from asphalt.templating.renderers.tornado import TornadoRenderer


@pytest.fixture
def renderer(request: FixtureRequest) -> TemplateRenderer:
    renderer_type = cast(str, request.param)
    if renderer_type == "django":
        return DjangoRenderer(package_paths=["tests/templates"])
    elif renderer_type == "mako":
        return MakoRenderer(package_paths=["tests/templates"])
    elif renderer_type == "jinja2":
        return Jinja2Renderer(package_name="tests")
    elif renderer_type == "tornado":
        return TornadoRenderer(package_path="tests/templates")


@pytest.mark.parametrize(
    "renderer, template_name",
    [
        pytest.param("jinja2", "jinja2.html", id="jinja2"),
        pytest.param("mako", "mako.mako", id="mako"),
        pytest.param("tornado", "tornado.html", id="tornado"),
    ],
    indirect=["renderer"],
)
class TestRenderer:
    def test_render(self, renderer: TemplateRenderer, template_name: str) -> None:
        result = renderer.render(template_name, testvar="åäö")
        assert (
            result.strip()
            == """\
<div>
    This is a sample
    Test variable: åäö
</div>"""
        )

    def test_render_string(
        self, renderer: TemplateRenderer, template_name: str
    ) -> None:
        source = (
            Path(__file__).with_name("templates").joinpath(template_name).read_text()
        )
        result = renderer.render_string(source, testvar="åäö")
        assert (
            result.strip()
            == """\
<div>
    This is a sample
    Test variable: åäö
</div>"""
        )


@pytest.mark.parametrize(
    "renderer, template_name",
    [
        pytest.param("jinja2", "jinja2_context.html", id="jinja2"),
        pytest.param("mako", "mako_context.mako", id="mako"),
        pytest.param("tornado", "tornado_context.html", id="tornado"),
    ],
    indirect=["renderer"],
)
@pytest.mark.asyncio
async def test_render(renderer: TemplateRenderer, template_name: str) -> None:
    async with Context() as ctx:
        ctx.add_resource("åäö")
        result = renderer.render(template_name, str=str)
        assert (
            result.strip()
            == """\
<div>
    This is a sample
    Test variable: åäö
</div>"""
        )
