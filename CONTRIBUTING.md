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

1. Fork and clone `django-bootstrap3` repo on GitHub. There is an excellent guide at <https://guides.github.com/activities/forking/>.
2. Install [poetry](https://python-poetry.org).
3. Inside your local `django-bootstrap3` folder, run
    ```shell script
    $ poetry install
    ```
4. Create a branch for local development:
    ```shell script
    $ git checkout -b name-of-your-bugfix-or-feature
    ```
    Now you can make your changes locally.
5. When you\'re done making changes, check that your changes pass the tests.
    Run the unit tests in your virtual environment with the `manage.py` command:
    ```shell script
    $ python manage.py test
    ````
    Run the extended tests with `tox`:
    ```shell script
    $ make tox
    ```
6. Commit your changes and push your branch to GitHub:
    ```shell script
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```
7. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in CHANGELOG.md.
3. The pull request should pass the Continuous Integration tests. Check <https://travis-ci.org/zostera/django-bootstrap3/pull_requests> and make sure that all tests pass. You can run the tests locally using `tox`.
