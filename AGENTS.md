# django-bootstrap3: Agent Guide

Bootstrap 3 template tags and filters for Django, by [Zostera](https://github.com/zostera).

## Maintenance mode

This package is in **maintenance mode**. Bootstrap 3 has been superseded by Bootstrap 4 and 5. Only bug fixes and security updates are accepted. Do not add new features or enhancements. Suggest Bootstrap 5 (`django-bootstrap5`) for new work.

Bootstrap 3 is EOL, no new releases are expected, but if they occur we will evaluate supporting them. Bootstrap 3 docs: https://getbootstrap.com/docs/3.4/

## Related packages

These packages share tooling and conventions. Changes in one often mirror to others:

- `https://github.com/zostera/django-bootstrap3`, Bootstrap 3 for Django (this package)
- `https://github.com/zostera/django-bootstrap4`, Bootstrap 4 for Django
- `https://github.com/zostera/django-bootstrap5`, Bootstrap 5 for Django
- `https://github.com/zostera/django-icons`, Icons for Django
- `https://github.com/zostera/django-marina`, Django extensions by Zostera

Config files (justfile, tox.ini, pyproject.toml, etc.) are kept in sync across packages.
AGENTS.md is **not** synced, each package has its own.

django-marina is the canonical source for this shared tooling. See its
[PACKAGING.md](https://github.com/zostera/django-marina/blob/main/PACKAGING.md) for exactly
which files sync, which need per-package substitution, and the propagation process.

## Setup

Requires [uv](https://github.com/astral-sh/uv) and [just](https://github.com/casey/just). Run `just` for the command list.

Never invoke `python`, `pip`, or `ruff` directly. All commands go through `just`, which delegates to `uv run` (venv) or `uvx` (ephemeral tools like ruff, twine, check-manifest).

`uv.lock` is fully generated, never manually resolve merge conflicts in it. On conflict: accept either side, then run `just upgrade` to regenerate.

Also run `just upgrade` after changing any dependency constraint in `pyproject.toml` (e.g. bumping the Django floor). Otherwise `uv.lock`'s own `requires-dist` metadata goes stale and silently drifts from `pyproject.toml`.

## Code style

ruff, configured in `[tool.ruff]` in `pyproject.toml`. `just format` fixes, `just lint` checks. Run it before committing, CI enforces it.

## Package structure

The package lives in `src/bootstrap3/`. The import and app name is `bootstrap3`, not `django_bootstrap3`, and template tags are loaded with `{% load bootstrap3 %}`.

## Testing

**Test runner is Django's test runner, not pytest.** Use `manage.py test` or `just test`.

The current Python × Django matrix is not a full grid. See `tox.ini`'s `envlist` for what's actually tested (`pyproject.toml` classifiers and `ci.yml`'s matrix must match it). Don't copy the matrix into prose elsewhere; it drifts. See [MAINTAINING.md](MAINTAINING.md) for the policy behind how the matrix is chosen and kept current.

Target the matrix when adding features; avoid Django-version-specific code paths where possible.

## CI

`just lint` must pass before committing, CI enforces it and will fail the PR.

See [MAINTAINING.md](MAINTAINING.md) for the release process and version-support policy.
