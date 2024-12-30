Configuration
=============

.. highlight:: yaml
.. py:currentmodule:: asphalt.templating

To configure a template renderer for your application, you need to choose a backend and
then specify any necessary configuration values for it. The following backends are
provided out of the box:

* ``django`` (:class:`.renderers.django.DjangoRenderer`)
* ``jinja2`` (:class:`.renderers.jinja2.Jinja2Renderer`)
* ``mako`` (:class:`.renderers.mako.MakoRenderer`)
* ``tornado`` (:class:`.renderers.tornado.TornadoRenderer`)

Other backends may be provided by other components.

Once you've selected a backend, see its specific documentation to find out what
configuration values you need to provide, if any. Configuration values are expressed as
constructor arguments for the backend class::

    components:
      templating:
        backend: mako
        options:
          package_paths:
            - myapp.somepackage/templates

This configuration publishes a :class:`TemplateRenderer` resource named ``default``.
The renderer will look for templates in the ``templates`` subdirectory of the
``myapp.somepackage`` package.

The same can be done directly in Python code as follows:

.. code-block:: python

    from asphalt.core import Component

    class ApplicationComponent(Component):
        async def start() -> None:
            self.add_component(
                "templating",
                backend="mako",
                options={"package_paths": ['myapp.somepackage/templates']}
            )
