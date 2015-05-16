import pytest
from pathlib import Path

from asphalt.templating.renderers.django import DjangoRenderer
from asphalt.templating.renderers.jinja2 import Jinja2Renderer
from asphalt.templating.renderers.mako import MakoRenderer
from asphalt.templating.renderers.tonnikala import TonnikalaRenderer
from asphalt.templating.renderers.tornado import TornadoRenderer


@pytest.fixture(params=['django', 'jinja2', 'mako', 'tonnikala', 'tornado'])
def renderer_type(request):
    return request.param


@pytest.fixture
def template_name(renderer_type):
    return {
        'django': 'django.html',
        'jinja2': 'jinja2.html',
        'mako': 'mako.mako',
        'tonnikala': 'tonnikala.tk',
        'tornado': 'tornado.html',
    }[renderer_type]


@pytest.fixture
def renderer(renderer_type):
    if renderer_type == 'django':
        return DjangoRenderer(package_paths=['tests/templates'])
    elif renderer_type == 'mako':
        return MakoRenderer(package_paths=['tests/templates'])
    elif renderer_type == 'jinja2':
        return Jinja2Renderer(package_name='tests')
    elif renderer_type == 'tonnikala':
        return TonnikalaRenderer(package_paths=['tests/templates'])
    elif renderer_type == 'tornado':
        return TornadoRenderer(package_path='tests/templates')


def test_render(renderer, template_name):
    result = renderer.render(template_name, testvar='åäö')
    assert result.strip() == """\
<div>
    This is a sample
    Test variable: åäö
</div>"""


def test_render_string(renderer, template_name):
    source = Path(__file__).with_name('templates').joinpath(template_name).read_text()
    result = renderer.render_string(source, testvar='åäö')
    assert result.strip() == """\
<div>
    This is a sample
    Test variable: åäö
</div>"""
