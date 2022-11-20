Configuration
=============

.. highlight:: yaml
.. py:currentmodule:: asphalt.templating

To configure a template renderer for your application, you need to choose a backend and
then specify any necessary configuration values for it. The following backends are
provided out of the box:

* :mod:`~.renderers.django`
* :mod:`~.renderers.jinja2`
* :mod:`~.renderers.mako`
* :mod:`~.renderers.tornado`

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

This configuration publishes a :class:`asphalt.templating.api.TemplateRenderer` resource
named ``default``. The renderer will look for templates in the ``templates``
subdirectory of the ``myapp.somepackage`` package.

The same can be done directly in Python code as follows:

.. code-block:: python

    class ApplicationComponent(ContainerComponent):
        async def start(ctx: Context) -> None:
            self.add_component(
                "templating",
                backend="mako",
                options={"package_paths": ['myapp.somepackage/templates']}
            )
            await super().start()


Multiple renderers
------------------

If you need to configure multiple renderers, you will need to use multiple instances
of the templating component::

    components:
      templating:
        backend: django
        options:
          package_paths:
            - myapp.somepackage/templates/django
      templating2:
        type: templating
        backend: jinja2
        resource_name: jinja2
        options:
          package_name: myapp.somepackage
          package_path: templates/jinja2
      templating3:
        type: templating
        backend: mako
        resource_name: mako
        options:
          package_paths:
            - myapp.somepackage/templates/mako

The above configuration creates 3 template renderer resources, available under 6
different combinations:

* :class:`~.api.TemplateRenderer` ``default`` (the Django renderer)
* :class:`~.renderers.django.DjangoRenderer` ``default`` (the Django renderer)
* :class:`~.api.TemplateRenderer` ``jinja2`` (the Jinja2 renderer)
* :class:`~.renderers.jinja2.Jinja2Renderer` ``jinja2`` (the Jinja 2 renderer)
* :class:`~.api.TemplateRenderer` ``mako`` (the Mako renderer)
* :class:`~.renderers.mako.MakoRenderer` ``mako`` (the Mako renderer)
