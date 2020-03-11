#!/usr/bin/env python

import setuptools
#TODO: somehow add completion scripts
setuptools.setup(
    name='pyjapi',
    description='JAPI client',
    long_description='',
    version='0.4.0',
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
    python_requires='>=3.6',
)
