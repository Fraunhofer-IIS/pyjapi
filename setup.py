#!/usr/bin/env python

import setuptools
from pyjapi import __version__

setuptools.setup(
    name='pyjapi',
    description='JAPI client',
    long_description="",
    version=__version__,
    author='Jannis Mainczyk',
    author_email='jannis.mainczyk@iis.fraunhofer.de',
    maintainer='Jannis Mainczyk',
    maintainer_email='jannis.mainczyk@iis.fraunhofer.de',
    url='https://git01.iis.fhg.de/mkj/pyjapi',
    keywords='japi,libjapi',
    license='',
    py_modules=['pyjapi'],
    entry_points='''
        [console_scripts]
        japi=pyjapi:cli
    ''',
    install_requires=['click>=7.0'],
    python_requires='>=3.6',
)
