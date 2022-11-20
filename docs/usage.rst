Using template renderers
========================

Using renderers is quite straightforward. For example, to render a Jinja2 template named
``templatefile.html``::

    from asphalt.core import inject, resource
    from asphalt.templating import TemplateRenderer

    @inject
    async def handler(*, renderer: TemplateRenderer = resource()):
        text = renderer.render("templatefile.html", somevariable="foo")

This example assumes a configuration with a Jinja2 renderer and a Jinja2 template file
named ``templatefile.html`` in the designated template directory.

To directly render a template string::

    @inject
    async def handler(*, renderer: TemplateRenderer = resource()):
        text = renderer.render_string('This is foo: {{ foo }}', somevariable='foo')

Using the current context in the template
-----------------------------------------

If an Asphalt context is active while a template is being rendered, that context will
be available to the template as the ``ctx`` variable.
