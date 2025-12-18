set export := true
set dotenv-load := true

alias update := upgrade
alias tox := tests

EXAMPLE_DIRNAME := "example"
VERSION := `sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`

# Default is to list commands and check if uv is installed
[private]
@default:
  just --list
  just uv

# Check to see if uv is installed
[private]
@uv:
    if ! command -v uv >/dev/null; then \
        echo "Error - Command 'uv' is not available."; \
        exit 1; \
    fi

# Delete the build directory and other build artefacts
[private]
@clean-build:
    rm -rf build dist src/*.egg-info .coverage*

# Delete the documentation build
[private]
@clean-docs:
    rm -rf docs/_build

# Check if the current Git branch is 'main'
[private]
@branch:
    if [ "`git rev-parse --abbrev-ref HEAD`" != "main" ]; then \
        echo "Error - Not on branch main."; \
        exit 1; \
    fi
    echo "On branch main.";

# Fail if working directory contains uncommitted or untracked changes
[private]
@porcelain:
    if [ -n "`git status --porcelain --untracked-files=all`" ]; then \
        echo "Error - Working directory is not clean. Commit your changes."; \
        exit 1; \
    fi
    echo "Working directory is clean.";

# Upgrade and install all dependencies
@upgrade: uv
    uv sync --all-extras --all-groups --upgrade

# Install all dependencies
@sync: uv
    uv sync --all-extras --all-groups --frozen

# Format source code
@format: uv
    uvx ruff format
    uvx ruff check --fix

# Check formatting of source code
@lint: uv
    uvx ruff format --check
    uvx ruff check

# Run test on the current environment with coverage and then report
@test *ARGS: sync
    just test-with-coverage-without-sync {{ARGS}}
    uv run coverage report

# Run test with coverage
[private]
@test-with-coverage-without-sync *ARGS:
    uv run coverage run manage.py test {{ARGS}}

# Run test command without coverage and syncing
[private]
@test-without-coverage-without-sync *ARGS:
    uv run manage.py test {{ARGS}}

# Run all tests (invokes tox)
@tests: sync
    uv run tox

# Build the package and test the build
@build: clean-build
    uv build
    uvx twine check dist/*
    uvx check-manifest
    uvx pyroma .
    uvx check-wheel-contents dist

# Build the documentation
@docs: clean-docs sync
    uv run -m sphinx -T -b html -d docs/_build/doctrees -D language=en docs docs/_build/html

# Run the example project
@example:
    if test -e {{ EXAMPLE_DIRNAME }}; then \
        cd "{{ EXAMPLE_DIRNAME }}" && python manage.py runserver; \
    else \
        echo "Example not found."; \
    fi

# Publish package on PyPI
@publish: porcelain branch docs build
    uvx uv-publish
    git tag -a v${VERSION} -m "Release {{ VERSION }}"
    git push origin --tags

# Show package version number
@version:
    echo "{{ VERSION }}"
