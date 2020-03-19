#!/usr/bin/env python

import setuptools
#TODO: somehow add completion scripts
setuptools.setup(
    name='pyjapi',
    description='JAPI client',
    long_description='',
    version='0.5.0',
    author='Jannis Mainczyk',
    author_email='jannis.mainczyk@iis.fraunhofer.de',
    maintainer='Jannis Mainczyk',
    maintainer_email='jannis.mainczyk@iis.fraunhofer.de',
    url='https://git01.iis.fhg.de/mkj/pyjapi',
    keywords='japi,libjapi,python,client',
    license='',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(exclude=['tests']),
    entry_points='''
        [console_scripts]
        japi=pyjapi.cli:cli
    ''',
    install_requires=['click>=7.0'],
    extras_require={
        'docs': [
            'sphinx',
            'sphinx-autobuild',
            'sphinxcontrib-confluencebuilder',  # git+https://github.com/sphinx-contrib/confluencebuilder.git
            'recommonmark',
            'sphinx-nameko-theme',
            'sphinx-click',
            'sphinx-automodapi',
            'sphinx-autodoc-typehints',
            'sphinxcontrib-programoutput',
            'sphinxcontrib-images',
            'sphinxcontrib-fulltoc',
            'sphinx-git',
            'jsonschema',  # required by jsonschemaext.py
        ],
        'dev': [
            'pycodestyle',
            'yapf',
            'pylint',
            'flake8',
            'pydocstyle',
            'coverage',
            'pytest',
            'pytest-cov',
        ],
    },
    python_requires='>=3.6',
)
