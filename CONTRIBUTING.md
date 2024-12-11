# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at <https://github.com/zostera/django-bootstrap3/issues>.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with \"bug\" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with \"feature\" is open to whoever wants to implement it.

### Write Documentation

`django-bootstrap3` could always use more documentation, whether as part of the official django-bootstrap3 docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
<https://github.com/zostera/django-bootstrap3/issues>.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.

## Get Started!

Ready to contribute? Here\'s how to set up `django-bootstrap3` for local development.

You will need some knowledge of git, github, and Python/Django development. Using a Python virtual environment is advised.

### Local installation

This package uses [uv](https://github.com/astral-sh/uv) and [just](https://github.com/casey/just).

After installing both, check out this repository and type `just bootstrap` to bootstrap a development environment.

```console
git clone git://github.com/zostera/django-bootstrap3.git
cd django-bootstrap3
just bootstrap
```

### Running the tests

To run the tests:

```console
just test
```

To run the tests on all supported Python/Django combinations:

```console
just tests
```

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests for new or changed functionality, and pass all tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in CHANGELOG.md.
