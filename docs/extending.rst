Writing new renderer backends
=============================

If you wish to implement an alternate method of template rendering, you can do so by subclassing
the :class:`~asphalt.templating.api.TemplateRenderer` class.
There is only one method implementors must override:

* :meth:`~asphalt.templating.api.TemplateRenderer.render`

If you want your renderer to be available as a backend for
:class:`~asphalt.templating.component.TemplatingComponent`, you need to add the corresponding
entry point for it. Suppose your serializer class is named ``AwesomeRenderer``, lives in the
package ``foo.bar.awesome`` and you want to give it the alias ``awesome``, add this line to your
project's ``setup.py`` under the ``entry_points`` argument in the ``asphalt.templating.renderers``
namespace::

    setup(
        # (...other arguments...)
        entry_points={
            'asphalt.templating.renderers': [
                'awesome = foo.bar.awesome:AwesomeRenderer'
            ]
        }
    )

