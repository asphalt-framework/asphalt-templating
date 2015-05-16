from asphalt.core.context import Context
import pytest

from asphalt.templating.api import TemplateRendererProxy
from asphalt.templating.component import TemplatingComponent


@pytest.mark.asyncio
async def test_single_renderer():
    ctx = Context()
    ctx.testvar = 'åäö'
    component = TemplatingComponent(backend='jinja2', package_name='tests')
    await component.start(ctx)

    assert isinstance(ctx.jinja2, TemplateRendererProxy)
    assert type(ctx.jinja2.environment).__name__ == 'Environment'
    assert ctx.jinja2.render('jinja2_context.html') == """\
<div>
    This is a sample
    Test variable: åäö
</div>"""
    assert ctx.jinja2.render_string('This is testvar: {{ ctx.testvar }}') == 'This is testvar: åäö'


@pytest.mark.asyncio
async def test_multiple_renderers():
    ctx = Context()
    ctx.testvar = 'åäö'
    component = TemplatingComponent({
        'jinja2': {'package_name': 'tests'},
        'mako': {'package_paths': ['tests/templates']}
    })
    await component.start(ctx)

    assert isinstance(ctx.jinja2, TemplateRendererProxy)
    assert isinstance(ctx.mako, TemplateRendererProxy)
