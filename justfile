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
  if ! command -v uv >/dev/null; then \
    echo "Error - Command 'uv' is not available. Please install uv."; \
    exit 1; \
  fi

# Upgrade and install all dependencies
@upgrade:
    uv sync --all-groups --upgrade

# Install for development (uses uv.lock)
install:
    uv sync --frozen --all-groups

# Format source code
@format:
    uvx ruff format
    uvx ruff check --fix

# Check formatting of source code
@lint:
    uvx ruff format --check
    uvx ruff check

# Run test with coverage
@test-cov *ARGS:
    uv run --no-sync coverage run manage.py test {{ARGS}}
    uv run --no-sync coverage report

# Run test
@test *ARGS:
    uv run --no-sync manage.py test {{ARGS}}

# Run all tests (invokes tox)
@tests *ARGS:
    uvx --with tox-uv tox {{ARGS}}

# Build the package and test the build
@build: clean-build install
    uv build
    uvx twine check dist/*
    uvx check-manifest
    uvx pyroma .
    uvx check-wheel-contents dist/*.whl

# Build the documentation
@docs: clean-docs install
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
