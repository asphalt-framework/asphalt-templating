import pytest
from asphalt.core.context import Context

from asphalt.templating.api import TemplateRenderer, TemplateRendererProxy
from asphalt.templating.component import TemplatingComponent


@pytest.mark.asyncio
async def test_single_renderer():
    async with Context() as ctx:
        ctx.add_resource("åäö")
        component = TemplatingComponent(
            backend="jinja2", options={"package_name": "tests"}
        )
        await component.start(ctx)

        renderer = ctx.require_resource(TemplateRenderer)
        assert isinstance(renderer, TemplateRendererProxy)

        assert type(renderer.environment).__name__ == "Environment"
        assert (
            renderer.render("jinja2_context.html", str=str)
            == """\
<div>
    This is a sample
    Test variable: åäö
</div>"""
        )
        assert (
            renderer.render_string(
                "This is testvar: {{ ctx.require_resource(str) }}", str=str
            )
            == "This is testvar: åäö"
        )
