#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import bootstrap3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = bootstrap3.__version__

if sys.argv[-1] == "publish":
    os.system("cd docs && make html")
    os.system("python setup.py sdist")
    os.system("twine upload dist/django-bootstrap3-{}.tar.gz".format(VERSION))

    message = "\nreleased [{version}](https://pypi.python.org/pypi/django-bootstrap3/{version})"
    print(message.format(version=VERSION))
    sys.exit()

if sys.argv[-1] == "test":
    print("Running tests only on current environment.")
    print("Use `tox` for testing multiple environments.")
    os.system("python manage.py test")
    sys.exit()

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read().replace(".. :changelog:", "")

setup(
    name="django-bootstrap3",
    version=VERSION,
    description="""Bootstrap support for Django projects""",
    long_description=readme + "\n\n" + history,
    author="Dylan Verheul",
    author_email="dylan@dyve.net",
    url="https://github.com/dyve/django-bootstrap3",
    packages=["bootstrap3"],
    include_package_data=True,
    install_requires=[],
    license="BSD-3-Clause",
    zip_safe=False,
    keywords="django-bootstrap3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
    ],
)
