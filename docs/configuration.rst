Configuration
=============

.. highlight:: yaml

To configure a template renderer for your application, you need to choose a backend and then
specify any necessary configuration values for it. The following backends are provided out of the
box:

* :mod:`~asphalt.templating.renderers.django`
* :mod:`~asphalt.templating.renderers.jinja2`
* :mod:`~asphalt.templating.renderers.mako`
* :mod:`~asphalt.templating.renderers.tonnikala`
* :mod:`~asphalt.templating.renderers.tornado`

Other backends may be provided by other components.

Once you've selected a backend, see its specific documentation to find out what configuration
values you need to provide, if any. Configuration values are expressed as constructor arguments
for the backend class::

    components:
      templating:
        backend: mako
        package_paths:
          - myapp.somepackage/templates

This configuration publishes a :class:`asphalt.templating.api.TemplateRenderer` lazy resource
named ``default`` using the Mako backend, accessible as ``ctx.mako``. The renderer will look for
templates in the ``templates`` subdirectory of the ``myapp.somepackage`` package.

The same can be done directly in Python code as follows::

    class ApplicationComponent(ContainerComponent):
        async def start(ctx: Context):
            self.add_component('templating', backend='mako',
                               package_paths=['myapp.somepackage/templates'])
            await super().start()


Note that the component API differs slightly for ``jinja2``. The call
to ``add_component`` for ``jinja2`` takes an optional ``loader_class`` argument
and arbitrary keyword arguments. All additional keyword arguments are
passed directly to the loader class. See the api documentation for more detail
regarding the options and defaults for the ``jinja2`` renderer, and be aware
that the acceptable keyword arguments will correspond to whatever
loader class you are using.

.. note::
    In Python, a keyword argument with the same name as an expected positional
    argument will be utilized for that positional argument. A function
    ``def some_func(a, b=None): pass`` can be called with
    ``some_func({'b': 'bar', 'a': 'foo'})``, in which case the value of ``a``
    will be ``foo``, and the value of ``b`` will be ``bar``.

A basic example of adding a ``jinja2`` rendering component is as follows. In
this example, the ``package_name`` keyword argument is passed to the default
``PackageLoader`` loader class as its first positional argument, and it will
then search for templates in ``myapp/templates`` by default::

    class ApplicationComponent(ContainerComponent):
        async def start(ctx: Context):
            self.add_component('templating', backend='jinja2',
                               package_name='myapp')
            await super().start()


Multiple renderers
------------------

If you need to configure multiple renderers, you can do so by using the ``renderers``
configuration option::

    components:
      templating:
        renderers:
          django:
            package_paths:
              - myapp.somepackage/templates/mako
          jinja2:
            package_name: myapp.somepackage
            package_path: templates/jinja2
          mako:
            package_paths:
              - myapp.somepackage/templates/mako
          tonnikala:
            package_paths:
              - myapp.somepackage/templates/tonnikala
          tornado:
            package_path: myapp.somepackage/templates/tornado
          foobar:
            backend: jinja2
            context_attr: foo
            package_name: myapp.somepackage
            package_path: templates/jinja2

The above configuration creates 5 lazy resources of type
:class:`asphalt.templating.api.TemplateRendererProxy`:

* ``django`` as ``ctx.django``
* ``jinja2`` as ``ctx.jinja2``
* ``mako`` as ``ctx.mako``
* ``tonnikala`` as ``ctx.tonnikala``
* ``tornado`` as ``ctx.tornado``
* ``foobar`` as ``ctx.foo``
