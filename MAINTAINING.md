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
- A pre-release goes in `tox.ini` and `ci.yml` but **not** in the `pyproject.toml` classifiers.
  A classifier is a promise to users, and a job that cannot fail the build does not back one.
  Add the classifier in the same change that makes the job blocking. Pair the pre-release only
  with the Django series that will support it first, the newest one plus `main`. A leg against
  a series that will never claim it is a standing red mark, and it teaches reviewers to ignore
  the column.

### Bootstrap

The default CDN URL is pinned to Bootstrap 3.4.1 — confirmed to be the final 3.x release
(Bootstrap itself has moved on to 5.x, no further 3.x releases are expected). Nothing to
monitor here under normal circumstances; only revisit if upstream unexpectedly cuts a new
3.x patch.

Don't put an upper bound on the `Django` dependency. A cap does not produce a clean failure when a
new Django major ships: the resolver backtracks to an older release of this package whose metadata
never had one, so users silently get old, unmaintained code instead of an error. Verified — asking
for `django-bootstrap4` with `django<5.2` resolves to `django-bootstrap4==26.1` with `django==5.1.15`,
no error. Capping the current release cannot close a door that published metadata already left open.

The `django-version: main` job in the CI matrix is the real early warning: it breaks while the new
major is still in development, when there is time to fix and release.

## Maintenance round

Start every maintenance round — and every release — by reconciling the support matrix with
reality, not from memory:

1. Check [endoflife.date/python](https://endoflife.date/python) and
   [endoflife.date/django](https://endoflife.date/django) for what is currently supported.
   The JSON endpoints (`https://endoflife.date/api/python.json`, `.../django.json`) are easier
   to diff against the matrix than the pages.
2. Drop every cycle that has gone EOL, and add every new one, per the policy above.
3. Reconcile all three sources of truth together — `tox.ini` (`envlist`),
   `.github/workflows/ci.yml` (`python_django_matrix`), and `pyproject.toml` (classifiers and
   the `Django` dependency). They drift independently, so check all three even when only one
   looks wrong.
4. Record any change as a `CHANGELOG.md` entry — dropping a cycle raises the dependency floor
   and is a breaking change for anyone on it. Under the `YY.N` version scheme the number
   carries no such signal, so the note is the only warning those users get.

## Release process

1. `just release-check` — lists the commits touching `src/` since the last tag next to the current
   `Unreleased` entries. Every one of those commits must be covered by an entry, or be a no-op for
   users (a docstring typo, say). A code change that reaches users without an entry ships invisible.
2. On a release branch, update `CHANGELOG.md` and bump `version` in `pyproject.toml`; open a PR and merge it
3. Check out and pull `main`
4. `just build` — builds wheel + tarball, runs packaging checks, and smoke-tests both against an isolated env
5. `just release-tag` — creates and pushes the version tag; GitHub Actions publishes to PyPI

`main` is protected — direct pushes are rejected (or bypass branch protection, which is worse). Always land the
version bump through a PR like any other change.

`just release-tag` requires a clean working directory and the current branch to be `main`. It will fail otherwise.

Order the release notes by category, in this order:

1. Security fixes
2. Dropped Python/Django cycles
3. Added Python/Django cycles
4. Bug fixes
5. Features
6. Tooling and internal changes
7. Everything else

The audience for these notes is someone upgrading, not someone shopping — so what might break
them comes before what is new for them. That is why fixes sort above features, unlike Keep a
Changelog, which lists Added first.

Security goes above even the support matrix: a user scanning the notes must not have to read
past a Django version line to find out they were vulnerable.

If an entry is a breaking behavior change rather than a plain fix — rendered output changes,
a default changes — prefix it with `**Breaking:**`. It sorts under bug fixes, where it would
otherwise read as routine.
