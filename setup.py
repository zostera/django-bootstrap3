#!/usr/bin/env python


import os
import sys

import bootstrap3

from setuptools import setup

VERSION = bootstrap3.__version__

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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
    ],
)
