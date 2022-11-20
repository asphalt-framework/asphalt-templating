Version history
===============

This library adheres to `Semantic Versioning 2.0 <http://semver.org/>`_.

**4.0.0** (2022-11-20)

- **BACKWARD INCOMPATIBLE** Bumped minimum Asphalt version to 4.8
- **BACKWARD INCOMPATIBLE** Refactored component to only provide a single renderer
  (you will have to add two components to get two renderers)
- **BACKWARD INCOMPATIBLE** Dropped the context attribute (use dependency injection
  instead)
- **BACKWARD INCOMPATIBLE** Template renderers are now added to the context directly,
  instead of being resource factories
- **BACKWARD INCOMPATIBLE** The ``ctx`` variable available to template renderers now
  corresponds to ``current_context()`` instead of the context they were created from
- Dropped explicit run-time type checking

**3.0.2** (2022-04-14)

- Added missing ``py.typed`` marker

**3.0.1** (2022-04-14)

- Fixed overly restrictive dependency constraint on Asphalt core

**3.0.0** (2021-12-27)

- **BACKWARD INCOMPATIBLE** Dropped Tonnikala support
- Added support for Python 3.10
- Dropped support for Python 3.5 and 3.6

**2.0.1** (2017-06-04)

- Added compatibility with Asphalt 4.0

**2.0.0** (2017-04-11)

- **BACKWARD INCOMPATIBLE** Migrated to Asphalt 3.0
- **BACKWARD INCOMPATIBLE** Renamed the ``asphalt.templating.util`` module to
  ``asphalt.templating.utils``
- Renderer resources are now added to the context using their actual types as well
- The Mako renderer now skips filesystem checks by default in production mode

**1.0.0** (2015-05-21)

- Initial release
