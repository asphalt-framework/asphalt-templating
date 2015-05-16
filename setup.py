from pathlib import Path

from setuptools import setup

setup(
    name='asphalt-templating',
    use_scm_version={
        'version_scheme': 'post-release',
        'local_scheme': 'dirty-tag'
    },
    description='Templating component for the Asphalt framework',
    long_description=Path(__file__).with_name('README.rst').read_text('utf-8'),
    author='Alex Grönholm',
    author_email='alex.gronholm@nextday.fi',
    url='https://github.com/asphalt-framework/asphalt-templating',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Text Processing :: General',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ],
    license='Apache License 2.0',
    zip_safe=False,
    packages=[
        'asphalt.templating',
        'asphalt.templating.renderers'
    ],
    setup_requires=[
        'setuptools_scm >= 1.7.0'
    ],
    install_requires=[
        'asphalt ~= 2.0'
    ],
    extras_require={
        'django': 'Django >= 1.9.0',
        'mako': 'Mako >= 1.0.1',
        'jinja2': 'Jinja2 >= 2.7.3',
        'tonnikala': 'tonnikala >= 1.0.0b1',
        'tornado': 'tornado >= 4.3.0'
    },
    entry_points={
        'asphalt.components': [
            'templating = asphalt.templating.component:TemplatingComponent'
        ],
        'asphalt.templating.renderers': [
            'django = asphalt.templating.renderers.django:DjangoRenderer [django]',
            'jinja2 = asphalt.templating.renderers.jinja2:Jinja2Renderer [jinja2]',
            'mako = asphalt.templating.renderers.mako:MakoRenderer [mako]',
            'tonnikala = asphalt.templating.renderers.mako:TonnikalaRenderer [tonnikala]',
            'tornado = asphalt.templating.renderers.tornado:TornadoRenderer [tornado]'
        ]
    }
)
