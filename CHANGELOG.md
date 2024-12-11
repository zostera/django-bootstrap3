# Changelog

## In development

- Add support for Python 3.13 (#1064, #1065).
- Use uv and just for package management (#1064).
- Drop support for Python 3.8 (EOL) (#1061).

## 24.3 (2024-09-18)

- Add support for Django 5.1 (#1013).

## 24.2 (2024-04-17)

- Reinstate setuptools_scm for build (#965).

## 24.1 (2024-04-16)

- Remove support for Django 3.2 (EOL) (#962).
- Remove setuptools_scm (#961).
- Fix Read the Docs (#958).

## 23.6 (2023-12-28)

- Use setuptools_scm to build package content (#920).

## 23.5 (2023-12-24)

- Fix Django versions in test matrix (#900).
- Use ruff instead of black for formatting (#901).
- Add support for Python 3.12 (#905).
- Add support for Django 5.0 (#904, #906).
- Revert packaging tools to setuptools, build, tox and twine (#908).

## 23.4 (2023-06-28)

- Fix inline form spacing (#892).

## 23.3 (2023-06-27)

- Fix example (#886).
- Remove support for Python 3.7 (EOL) (#889).
- Fix radio buttons in Django 4 (#887).
- Fix check order of CheckboxSelectMultiple and RadioSelect (#859).

## 23.2 (2023-06-08)

- Switch to Hatch (#880).
- Reinstate coveralls (#880).
- Fix readthedocs config (#844).
- Remove version restriction on importlib-metadata (#843).
- Replace m2r2 with sphinx-mdinclude (#842).
- Update packaging, reduce dependencies (#849).
- Drop support for Django 4.0 (#849).
- Fix example (#853).

## 23.1 (2023-04-02)

- Add support for Django 4.2 (#828).
- Update requirements and packages (#828).
- Stop using coveralls (#829).

## 22.2 (2022-11-22)

- Add support Python 3.11 (#775).

## 22.1 (2022-08-08)

- Add support for Django 4.1 (#718).
- Drop support for Django 2.2 (EOL) (#718).

## 21.2 (2021-12-27)

- Drop support for Django 3.1 (EOL, #632).
- Drop support for Python 3.6 (EOL, #632).
- Fix CI (#632).

## 21.1 (2021-11-03)

- Switch to a [CalVer](https://calver.org) YY.MINOR versioning scheme. MINOR is the number of the release in the given year. This is the first release in 2021 using this scheme, so its version is 21.1. The next version this year will be 21.2. The first version in 2022 will be 22.1.
- Add support for Django 4 and Python 3.10 (#579).
## 15.0.0 (2021-04-10)

- Drop support for Django 3.0, extended support stopped on 2021-04-01).
- Add support for Django 3.2.
- Fix `render_alert` (#488)
- Rename AUTHORS.md to AUTHORS, remove authors section from documentation.
- Revert to setuptools for packaging.
- Add docs and tests to sdist (#494).
- Use GitHub Actions for CI.

## 14.2.0 (2020-10-13)

- Reformat CHANGELOG.
- Fix Django 3.1 warning in test app settings.
- Update black.
- Replace m2r with m2r2 to support Sphinx3.
- Add Python 3.9 to test matrix.

## 14.1.0 (2020-07-02)

- Fix coveralls.
- Explicitly support Django 3.1 in tox matrix.

## 14.0.0 (2020-06-22)

- Drop support for Python 3.5 and Django 2.1.
- Use Poetry (https://python-poetry.org/) for dependency management and packaging.
- Change documentation to support main branch rename to 'main'.
- Fix settings override bug (fixes #388).
- Use Markdown for README.
- Fix Travis, ReadTheDocs and tox configurations.
- Update Makefile with lessons learned from other packages.

## 12.1.0 (2020-05-01)

- Distinguish between help text and errors (fixes #479)

## 12.0.3 (2019-12-21)

- Update changelog

## 12.0.2 (2019-12-21)

- Revert of #453, which turned out to break checkboxes (fixes #467)
- Update requirements and fix `make docs`
- Replace `force_text` with `force_str`, removes warnings

## 12.0.1 (2019-12-12)

- Reinstate ``bootstrap3.__version__`` (fixes #486)
- Update Makefile, travis and tox configuration (#470)

## 12.0.0 (2019-12-04)

- Drop support for Python 2.7, Django 1.11 and Django 2.0 (#456)
- Fix Deprecationwarning in Python 3.7 (#455)
- Add label class support to form field checkboxes (#453)
- Move development tasks from `setup.py` to `Makefile`
- Fix compatibility with Django 3.0 and master
- Add Django 3.0 to `tox.ini`
- Update versions in `requirements.txt`
- Use Makefile for common tasks
- Drop `MANIFEST.in`, use `setuptools_scm`
- Drop `_version.py`, use version from git tag

## 11.1.0 (2019-08-09)

- Update Bootstrap to 3.4.1 (#459)
- **NOTE** Version 12 will drop support for Python 2.x.x and Django 1.x.x

## 11.0.0 (2018-08-30)

- Support `crossorigin` and `integrity` in urls (#443)
- Switch to explicit Travis tests (#444)
- Fix PyPI classifiers
- Remove obsolete code for Django <= 1.8 (#446)
- Remove obsolete settings `set_required` and `set_disabled` (#445)
- Remove setting `base_url` (#443)

## 10.0.1 (2018-05-02)

- Fix PyPI classifiers

## 10.0.0 (2018-05-01)

- Drop support for Django 1.8 (#434)
- Fix bug in demo app (#430)
- Remove unnecessary `len` call (#424)
- Switched to master as main branch, deleted other branches
- Switched to twine for publication on PyPI

## 9.1.0 (2017-10-27)

- Mention django-bootstrap4 (https://github.com/zostera/django-bootstrap4) in README
- Rewrite `tox` test matrix to focus on Django releases rather than Python versions
- Add tests for Django master branch (>= 2)
- Add `label` override for `{% bootstrap_field %}`

## 9.0.0 (2017-07-11)

- Renamed requirements-dev.txt back to requirements.txt because that suits ReadTheDocs better
- Added `error_types` support on `bootstrap3_form` (thanks @mkoistinen and @ickam)
- **BREAKING** Default setting of `error_types` to `non_field_errors` is different from behavior in versions < 9

## 8.2.3 (2017-05-05)

- Renamed requirements.txt to requirements-dev.txt
- Tweaks to tests and CI (see #400)
- Prepared test for geometry fields (disabled, blocked by Django update, see #392)
- Bug fixes for add ons and placeholders (thanks @jaimesanz, @cybojenix and @marc-gist)
- Improve documentation for pagination with GET parameters (thanks @nspo)
- Add unicode test for help_text
- Removed tests for Python 3.2 from tox and Travis CI (no longer supported by Django 1.8)

## 8.2.2 (2017-04-03)

- Fix invalid HTML in help texts (thanks @luksen)
- Added `mark_safe` to placeholder (thanks @ppo)
- Fix DateWidget import for newer Django versions (thanks @clokep)

## 8.2.1 (2017-02-23)

- Support for local languages in `url_replace_param` on Python 2 (#362, thanks @aamalev)
- Correct checking Mapping instance (#363, thanks @aamalev)
- Fix Django 1.11 import bug (see #369)
- Add Django 1.11 and Python 3.6 to tests
- Fix sdist issue with .pyc files

## 8.1.0 (2017-01-12)

- Rolled back subresource integrity (see #353)
- Documentation fix (thanks @clokep)

## 8.0.0 (2017-01-06)

- **BREAKING** For Django >= 1.10 Remove everything to do with setting HTML attributes `required` (#337) and `disabled` (#345)
- Add `id` parameter to bootstrap_button (#214)
- Add `set_placeholder` to field and form renderers (#339, thanks @predatell)
- Default button type to `btn-default`
- Add `addon_before_class` and `addon_after_class` (#295, thanks @DanWright91 and others)
- Fix handling of error class (#170)
- No size class for checkboxes (#318, thanks @cybojenix)
- Fix warnings during install (thanks @mfcovington)
- Fix rare RunTimeError when working without database (#346, thanks @Mactory)
- Add subresource integrity to external components (thanks @mfcovington and @Alex131089)
- Several improvements to documentation, tests, and comments. Thanks all!

## 7.1.0 (2016-09-16)

- Print help text and errors in their own block (#329, thanks @Matoking)
- Improved page urls in pagination (fixes #323)
- Changed setup.py to allow `setup.py test` run tests
- Removed link target from active page in pagination (fixes #328)
- Fixed example for bootstrap_label (fixed #332)
- Fixed tests to support Django 1.10 handling of required attribute, see #337 (needs fixing)
- Added tests for Django 1.10
- Bootstrap to 3.3.7

## 7.0.1 (2016-03-23)

- Fixed bug with widget attrs consistency (@onysos)

## 7.0.0 (2016-02-24)

- Dropped support for Django < 1.8
- Dropped support for Python < 2.7
- Fix page number bug (thanks @frewsxcv)
- Fix template context warning (thanks @jieter and @jonashaag)
- Update to Bootstrap 3.3.6 (@nikolas)
- Show links and newlines in messages (@jakub3279)
- CSS classes arguments passed to the bootstrap_form are now working (@gordon)
- Support for Django 1.9/Python 3.5 (@jieter and @jonashaag)
- Better Travis CI Django versions (thanks @jonashaag)
- Improved handling of messages in `bootstrap_messages` (thanks @frewsxcv and @rjsparks)

## 6.2.2 (2015-08-20)

- Bug fix for escaped icons in buttons (reported by @jlec)

## 6.2.1 (2015-08-19)

- Bug fix for whitespace in label placeholders (@Grelek)

## 6.2.0 (2015-08-15)

- Improved tests
- Make simple_tag output safe in Django 1.9
- Better support for MultiWidgets (@xrmx)
- Better documentation (@Moustacha)

## 6.1.0 (2015-06-25)

- Upgrade to Bootstrap 3.3.5
- Properly quote help text (@joshkel)

## 6.0.0 (2015-04-21)

- No more media="screen" in CSS tags, complying to Bootstraps examples

## 5.4.0 (2015-04-21)

- No more forcing btn-primary when another button class is specified (@takuchanno2)
- Added value option to buttons (@TyVik)
- Switched CDN to //maxcdn.bootstrapcdn.com/bootstrap/3.3.4/ (@djangoic)

## 5.3.1 (2015-04-08)

- Fix Django 1.8 importlib warnings
- Set defaults for horizontal-form to col-md-3 for label, col-md-9 for field
- Various bug fixes
- Fix version number typo

## 5.2.0 (2015-03-25)

- Upgrade to Bootstrap 3.3.4
- Fix required bug for checkboxes
- Various bug fixes

## 5.1.1 (2015-01-22)

- Fix checkbox display bug

## 5.1.0 (2015-01-22)

- Make Bootstrap 3.3.2 default
- Fix issue #140 (bad behaviour in Python 3)

## 5.0.3 (2014-12-02)

- Fixing tests for older Django and Python versions

## 5.0.2 (2014-11-24)

- Cleaning up some mess in 5.0.1 created by PyPI malfunction

## 5.0.1 (2014-11-21)

- Bug fixes and update to Bootstrap 3.3.1

## 4.11.0 (2014-08-19)

- Improved handling and control of form classes for error and success

## 4.10.1 (2014-08-18)

- Bug fixes, test fixes, documentation fixes

## 4.10.0 (2014-08-12)

- Template tag `bootstrap_icon` now supports a `title` parameter

## 4.9.2 (2014-08-11)

- Fixed bug causing problems with setting classes for horizontal forms

## 4.9.1 (2014-08-10)

- Fixed test for Django 1.4

## 4.9.0 (2014-08-09)

- New parameter `href` for `bootstrap_button`, if provided will render `a` tag instead of `button` tag

## 4.8.2 (2014-07-10)

- Internal fixes to master branch

## 4.8.1 (2014-07-10)

- Make extra classes override bootstrap defaults

## 4.8.0 (2014-07-10)

- Introduced new setting `set_placeholder`, default True

## 4.7.1 (2014-07-07)

- Fixed rendering of various sizes (as introduced in 4.7.0)
- Upgrade to Bootstrap 3.2.0 as default version

## 4.7.0 (2014-06-04)

- `size` option added to formsets, forms, fields and buttons

## 4.6.0 (2014-05-22)

- new `bootstrap_formset_errors` tag

## 4.5.0 (2014-05-21)

- bug fixes in formsets
- new formset renderer
- new `bootstrap_form_errors` tag

## 4.4.2 (2014-05-20)

- documentation now mentions templates

## 4.4.1 (2014-05-08)

- bug fixes
- documentation fixes
- test coverage on coveralls.io

## 4.4.0 (2014-05-01)

- added `bootstrap_alert` template tag

## 4.3.0 (2014-04-25)

- added `required_css_class` and `error_css_class` as optional settings (global) and parameters (form and field rendering)

## 4.2.0 (2014-04-06)

- moved styling of form level errors to template
- bug fixes

## 4.1.1 (2014-04-06)

- moved all text conversions to text_value

## 4.1.0 (2014-04-05)

- typo fix and internal branching changes

## 4.0.3 (2014-04-03)

- fixed checkbox label bug in vertical and inline forms

## 4.0.2 (2014-04-02)

- fixed bug in vertical form rendering

## 4.0.1 (2014-03-29)

- fixed unicode bug and added unicode label to tests

## 4.0.0 (2014-03-28)

- use renderer classes for generating HTML
- several bug fixes

## 3.3.0 (2014-03-19)

- use Django forms css classes for indicating required and error on fields

## 3.2.1 (2014-03-16)

- improved form rendering

## 3.2.0 (2014-03-11)

- support for addons

## 3.1.0 (2014-03-03)

- improve compatibility with Django < 1.5

## 3.0.0 (2014-02-28)

- added support for themes (fix issue #74)
- show inline form errors in field title (fix issue #81)
- fixed bugs in demo application
- update to newest Bootstrap (fix issue #83)

## 2.6.0 (2014-02-20)

- new setting `set_required` to control setting of HTML `required` attribute (fix issue #76)

## 2.5.6 (2014-01-23)

- project refactored
- added skeleton for creating documentation (fix issue #30)
- fixed `FileField` issues
