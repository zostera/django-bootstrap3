# django-bootstrap3 — Agent Guide

Bootstrap 3 template tags and filters for Django, by [Zostera](https://github.com/zostera).

## Maintenance mode

This package is in **maintenance mode** — Bootstrap 3 has been superseded by Bootstrap 4 and 5. Only bug fixes and security updates are accepted. Do not add new features or enhancements. Suggest Bootstrap 5 (`django-bootstrap5`) for new work.

Bootstrap 3 is EOL — no new releases are expected, but if they occur we will evaluate supporting them. Bootstrap 3 docs: https://getbootstrap.com/docs/3.4/

## Related packages

These packages share tooling and conventions — changes in one often mirror to others:

- `https://github.com/zostera/django-bootstrap3` — Bootstrap 3 for Django (this package)
- `https://github.com/zostera/django-bootstrap4` — Bootstrap 4 for Django
- `https://github.com/zostera/django-bootstrap5` — Bootstrap 5 for Django
- `https://github.com/zostera/django-icons` — Icons for Django
- `https://github.com/zostera/django-marina` — Django extensions by Zostera

Config files (justfile, tox.ini, pyproject.toml, etc.) are kept in sync across packages.
AGENTS.md is **not** synced — each package has its own.

## Setup

Requires [uv](https://github.com/astral-sh/uv) and [just](https://github.com/casey/just).

```
just install    # install deps from uv.lock
just upgrade    # upgrade all deps
```

Never invoke `python`, `pip`, or `ruff` directly. All commands go through `just`, which delegates to `uv run` (venv) or `uvx` (ephemeral tools like ruff, twine, check-manifest).

`uv.lock` is fully generated — never manually resolve merge conflicts in it. On conflict: accept either side, then run `just upgrade` to regenerate.

## Key commands

```
just test           # run tests (single Python/Django version)
just test-cov       # run tests with coverage report
just tests          # run full tox matrix (all Python × Django combos)
just lint           # check formatting and style (ruff)
just format         # auto-fix formatting and style
just build          # build + packaging checks (preflight before release)
just docs           # build Sphinx documentation
just example        # run the example Django project
just version        # print current package version
```

## Code style

- **Formatter/linter**: ruff (line length 120)
- **Docstrings**: pydocstyle D2xx/D4xx rules; D1xx (missing docstring) is ignored
- `ruff check --fix` auto-fixes isort, pyupgrade, and some flake8 issues
- `F8` (unused names) is not auto-fixed — fix manually

Run `just lint` before committing. CI enforces it.

## Package structure

```
src/bootstrap3/
    __about__.py        version string
    __init__.py         exports __version__
    bootstrap.py        settings access and URL helpers (css_url, javascript_url, etc.)
    components.py       alert and icon renderers
    exceptions.py       custom exceptions
    forms.py            form and field rendering functions
    models.py           model helpers
    renderers.py        field and form renderer classes
    text.py             text utilities
    utils.py            template and HTML utilities
    templatetags/
        bootstrap3.py   all template tags and filters
    templates/bootstrap3/
        *.html          component templates (messages, pagination, field errors, etc.)
```

## Testing

**Test runner is Django's test runner, not pytest.** Use `manage.py test` or `just test`.

```
tests/
    app/                minimal Django project used as test harness
        settings.py
        urls.py
        forms.py
    smoke_test.py       import smoke test (run against built wheel/tarball)
    test_settings.py
    test_templates.py
    test_templatetags.py
    test_version.py
```

Test matrix (tox) — not a full grid:

| Python  | Django versions         |
|---------|-------------------------|
| 3.10    | 4.2, 5.2                |
| 3.11    | 4.2, 5.2                |
| 3.12    | 4.2, 5.2, 6.0, main     |
| 3.13    | 4.2, 5.2, 6.0, main     |
| 3.14    | 5.2, 6.0, main          |

Target the matrix when adding features; avoid Django-version-specific code paths where possible.

## CI

GitHub Actions runs on every push and PR:
- `ci.yml` — lint + full tox matrix
- `release.yml` — publishes to PyPI on version tags

`just lint` must pass before committing — CI enforces it and will fail the PR.

## Release process

1. Update `CHANGELOG.md` and bump `version` in `pyproject.toml`
2. Commit and push to `main`
3. `just build` — builds wheel + tarball, runs packaging checks, and smoke-tests both against an isolated env
4. `just release-tag` — creates and pushes the version tag; GitHub Actions publishes to PyPI

`just release-tag` requires: clean working directory AND current branch is `main`. It will fail otherwise.
