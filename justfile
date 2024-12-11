set export := true
set dotenv-load := true

EXAMPLE_DIRNAME := "example"
VENV_DIRNAME := ".venv"
VERSION := `sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`

# default recipe
default:
    just --list

[private]
@uv:
    if ! command -v uv >/dev/null; then \
        echo "Error: 'uv' command is not available"; \
        exit 1; \
    fi

# Set up development environment
@bootstrap: uv
    if test ! -e {{ VENV_DIRNAME }}; then \
        uv python install; \
    fi
    just update

# Install and/or update all dependencies defined in pyproject.toml
@update: uv
    uv sync --all-extras --all-groups --upgrade

# Format
@format: bootstrap
    ruff format
    ruff check --fix

# Lint
@lint: bootstrap
    ruff format --check
    ruff check

# Test
@test: bootstrap
    coverage run manage.py test
    coverage report

# Test
@tests: bootstrap
    tox

# Build
@build: bootstrap
    uv build
    uvx twine check dist/*
    uvx check-manifest
    uvx pyroma .
    uvx check-wheel-contents dist

# Clean
@clean:
    rm -rf build dist src/*.egg-info .coverage*

# Check if the current Git branch is 'main'
@branch:
    if [ "`git rev-parse --abbrev-ref HEAD`" = "main" ]; then \
        echo "On branch main."; \
    else \
        echo "Error - Not on branch main."; \
        exit 1; \
    fi

# Check if the working directory is clean
@porcelain:
    if [ -z "`git status --porcelain`" ]; then \
        echo "Working directory is clean."; \
    else \
        echo "Error - working directory is dirty. Commit your changes."; \
        exit 1; \
    fi

@docs: bootstrap clean
    uv run -m sphinx -T -b html -d docs/_build/doctrees -D language=en docs docs/_build/html

@example:
    if test -e {{ EXAMPLE_DIRNAME }}; then \
        cd "{{ EXAMPLE_DIRNAME }}" && python manage.py runserver; \
    else \
        echo "Example not found."; \
    fi

@publish: porcelain branch docs build
    uvx uv-publish
    git tag -a v${VERSION} -m "Release {{ VERSION }}"
    git push origin --tags

# Version number
@version:
    echo "{{ VERSION }}"
