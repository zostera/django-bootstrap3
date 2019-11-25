#!/usr/local/bin/python


import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme_file:
    readme = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), "HISTORY.rst")) as history_file:
    history = history_file.read().replace(".. :changelog:", "")


setup(
    name="django-bootstrap3",
    description="""Bootstrap support for Django projects""",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    author="Dylan Verheul",
    author_email="dylan@dyve.net",
    url="https://github.com/dyve/django-bootstrap3",
    license="BSD-3-Clause",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
    keywords="django-bootstrap3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
