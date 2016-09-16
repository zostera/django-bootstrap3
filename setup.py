#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import bootstrap3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = bootstrap3.__version__

if sys.argv[-1] == 'publish':
    os.system('cd docs && make html')
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

if sys.argv[-1] == 'test':
    print("Running tests only on current environment.")
    print("Use `tox` for testing multiple environments.")
    os.system('python manage.py test')
    sys.exit()

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='django-bootstrap3',
    version=version,
    description="""Bootstrap support for Django projects""",
    long_description=readme + '\n\n' + history,
    author='Dylan Verheul',
    author_email='dylan@dyve.net',
    url='https://github.com/dyve/django-bootstrap3',
    packages=[
        'bootstrap3',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="Apache License 2.0",
    zip_safe=False,
    keywords='django-bootstrap3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
