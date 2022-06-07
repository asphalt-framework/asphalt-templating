Writing new renderer backends
=============================

.. highlight:: toml

If you wish to implement an alternate method of template rendering, you can do so by
subclassing the :class:`~asphalt.templating.api.TemplateRenderer` class.
There are two methods implementors must override:

* :meth:`~asphalt.templating.api.TemplateRenderer.render`
* :meth:`~asphalt.templating.api.TemplateRenderer.render_string`

If you want your renderer to be available as a backend for
:class:`~asphalt.templating.component.TemplatingComponent`, you need to add the
corresponding entry point for it. Suppose your template renderer class is named
``AwesomeRenderer``, lives in the package ``foo.bar.awesome`` and you want to give it
the alias ``awesome``, add this line to your project's ``pyproject.toml`` under the
``entry_points`` argument in the ``asphalt.templating.renderers`` namespace::

    [project.entry-points."asphalt.templating.renderers"]
    awesome = "foo.bar.awesome:AwesomeRenderer"
