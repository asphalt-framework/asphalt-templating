Using template renderers
========================

Using renderers is quite straightforward. For example, to render a Jinja2 template named
``templatefile.html``::

    async def handler(ctx):
        text = ctx.jinja2.render('templatefile.html', somevariable='foo')

This example assumes a configuration with a Jinja2 renderer and a Jinja2 template file named
``templatefile.html`` in the designated template directory.

To directly render a template string::

    async def handler(ctx):
        text = ctx.jinja2.render_string('This is foo: {{ foo }}', somevariable='foo')
