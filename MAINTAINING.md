# Maintaining django-bootstrap3

Notes for maintainers. For how to submit a contribution, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Maintenance mode

This package is in maintenance mode (see AGENTS.md and CONTRIBUTING.md) — only bug fixes,
security updates, and Python/Django compatibility are in scope. The policy below still
applies to compatibility work even though the package accepts no new features.

## Version support policy

These are rules, not a snapshot of current versions — the current matrix lives in `tox.ini`
(`envlist`), `.github/workflows/ci.yml` (the `python_django_matrix` job), and `pyproject.toml`
(classifiers + `dependencies`). Those three files are the source of truth and must agree with
each other. Don't restate the matrix as a table in prose docs (AGENTS.md, README, etc.) — a
copy always drifts out of sync with the files that actually enforce it.

- Support every Python and Django release cycle that is not end-of-life, per
  [endoflife.date/python](https://endoflife.date/python) and
  [endoflife.date/django](https://endoflife.date/django). Drop a cycle from the matrix as soon
  as it goes EOL — don't wait for a scheduled release to do it.
- Always track Django's `main` branch in the matrix. Add a new Django release series
  (e.g. 6.1) alongside `main` as soon as `main` has diverged from it — i.e. once upstream
  cuts a `stable/X.Y.x` branch and `main` itself moves on to the next alpha. Don't wait for
  the new series' final release.
- Add a new Python pre-release as a **non-blocking** CI job (`continue-on-error: true`) as
  soon as it's installable — `uv python install` can usually fetch a new CPython the same day
  it's cut, so the interpreter itself is rarely the blocker. Only make the job blocking once
  test dependencies with C extensions publish wheels for it, if any are in use.

## Release process

1. Update `CHANGELOG.md` and bump `version` in `pyproject.toml`
2. Commit and push to `main`
3. `just build` — builds wheel + tarball, runs packaging checks, and smoke-tests both against an isolated env
4. `just release-tag` — creates and pushes the version tag; GitHub Actions publishes to PyPI

`just release-tag` requires a clean working directory and the current branch to be `main`. It will fail otherwise.
