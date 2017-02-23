.. :changelog:

History
-------


8.2.1 (2017-02-23)
++++++++++++++++++

* Support for local languages in `url_replace_param` on Python 2 (#362, thanks @aamalev)
* Correct checking Mapping instance (#363, thanks @aamalev)
* Fix Django 1.11 import bug (see #369)
* Add Django 1.11 and Python 3.6 to tests
* Fix sdist issue with .pyc files


8.1.0 (2017-01-12)
++++++++++++++++++

* Rolled back subresource integrity (see #353)
* Documentation fix (thanks @clokep)


8.0.0 (2017-01-06)
++++++++++++++++++

* **BREAKING** For Django >= 1.10 Remove everything to do with setting HTML attributes `required` (#337) and `disabled` (#345)
* Add `id` parameter to bootstrap_button (#214)
* Add `set_placeholder` to field and form renderers (#339, thanks @predatell)
* Default button type to `btn-default`
* Add `addon_before_class` and `addon_after_class` (#295, thanks @DanWright91 and others)
* Fix handling of error class (#170)
* No size class for checkboxes (#318, thanks @cybojenix)
* Fix warnings during install (thanks @mfcovington)
* Fix rare RunTimeError when working without database (#346, thanks @Mactory)
* Add subresource integrity to external components (thanks @mfcovington and @Alex131089)
* Several improvements to documentation, tests, and comments. Thanks all!


7.1.0 (2016-09-16)
++++++++++++++++++

* Print help text and errors in their own block (#329, thanks @Matoking)
* Improved page urls in pagination (fixes #323)
* Changed setup.py to allow `setup.py test` run tests
* Removed link target from active page in pagination (fixes #328)
* Fixed example for bootstrap_label (fixed #332)
* Fixed tests to support Django 1.10 handling of required attribute, see #337 (needs fixing)
* Added tests for Django 1.10
* Bootstrap to 3.3.7


7.0.1 (2016-03-23)
++++++++++++++++++

* Fixed bug with widget attrs consistency (@onysos)


7.0.0 (2016-02-24)
++++++++++++++++++

* Dropped support for Django < 1.8
* Dropped support for Python < 2.7
* Fix page number bug (thanks @frewsxcv)
* Fix template context warning (thanks @jieter and @jonashaag)
* Update to Bootstrap 3.3.6 (@nikolas)
* Show links and newlines in messages (@jakub3279)
* CSS classes arguments passed to the bootstrap_form are now working (@gordon)
* Support for Django 1.9/Python 3.5 (@jieter and @jonashaag)
* Better Travis CI Django versions (thanks @jonashaag)
* Improved handling of messages in `bootstrap_messages` (thanks @frewsxcv and @rjsparks)


6.2.2 (2015-08-20)
++++++++++++++++++

* Bug fix for escaped icons in buttons (reported by @jlec)


6.2.1 (2015-08-19)
++++++++++++++++++

* Bug fix for whitespace in label placeholders (@Grelek)


6.2.0 (2015-08-15)
++++++++++++++++++

* Improved tests
* Make simple_tag output safe in Django 1.9
* Better support for MultiWidgets (@xrmx)
* Better documentation (@Moustacha)


6.1.0 (2015-06-25)
++++++++++++++++++

* Upgrade to Bootstrap 3.3.5
* Properly quote help text (@joshkel)


6.0.0 (2015-04-21)
++++++++++++++++++

* No more media="screen" in CSS tags, complying to Bootstraps examples


5.4.0 (2015-04-21)
++++++++++++++++++

* No more forcing btn-primary when another button class is specified (@takuchanno2)
* Added value option to buttons (@TyVik)
* Switched CDN to //maxcdn.bootstrapcdn.com/bootstrap/3.3.4/ (@djangoic)


5.3.1 (2015-04-08)
++++++++++++++++++

* Fix Django 1.8 importlib warnings
* Set defaults for horizontal-form to col-md-3 for label, col-md-9 for field
* Various bug fixes
* Fix version number typo


5.2.0 (2015-03-25)
++++++++++++++++++

* Upgrade to Bootstrap 3.3.4
* Fix required bug for checkboxes
* Various bug fixes


5.1.1 (2015-01-22)
++++++++++++++++++

* Fix checkbox display bug


5.1.0 (2015-01-22)
++++++++++++++++++

* Make Bootstrap 3.3.2 default
* Fix issue #140 (bad behaviour in Python 3)


5.0.3 (2014-12-02)
++++++++++++++++++

* Fixing tests for older Django and Python versions


5.0.2 (2014-11-24)
++++++++++++++++++

* Cleaning up some mess in 5.0.1 created by PyPI malfunction


5.0.1 (2014-11-21)
++++++++++++++++++

* Bug fixes and update to Bootstrap 3.3.1


4.11.0 (2014-08-19)
+++++++++++++++++++

* Improved handling and control of form classes for error and success


4.10.1 (2014-08-18)
+++++++++++++++++++

* Bug fixes, test fixes, documentation fixes


4.10.0 (2014-08-12)
+++++++++++++++++++

* Template tag `bootstrap_icon` now supports a `title` parameter


4.9.2 (2014-08-11)
++++++++++++++++++

* Fixed bug causing problems with setting classes for horizontal forms


4.9.1 (2014-08-10)
++++++++++++++++++

* Fixed test for Django 1.4


4.9.0 (2014-08-09)
++++++++++++++++++

* New parameter `href` for `bootstrap_button`, if provided will render `a` tag instead of `button` tag


4.8.2 (2014-07-10)
++++++++++++++++++

* Internal fixes to master branch


4.8.1 (2014-07-10)
++++++++++++++++++

* Make extra classes override bootstrap defaults


4.8.0 (2014-07-10)
++++++++++++++++++

* Introduced new setting `set_placeholder`, default True


4.7.1 (2014-07-07)
++++++++++++++++++

* Fixed rendering of various sizes (as introduced in 4.7.0)
* Upgrade to Bootstrap 3.2.0 as default version


4.7.0 (2014-06-04)
++++++++++++++++++

* `size` option added to formsets, forms, fields and buttons


4.6.0 (2014-05-22)
++++++++++++++++++

* new `bootstrap_formset_errors` tag


4.5.0 (2014-05-21)
++++++++++++++++++

* bug fixes in formsets
* new formset renderer
* new `bootstrap_form_errors` tag


4.4.2 (2014-05-20)
++++++++++++++++++

* documentation now mentions templates


4.4.1 (2014-05-08)
++++++++++++++++++

* bug fixes
* documentation fixes
* test coverage on coveralls.io


4.4.0 (2014-05-01)
++++++++++++++++++

* added `bootstrap_alert` template tag


4.3.0 (2014-04-25)
++++++++++++++++++

* added `required_css_class` and `error_css_class` as optional settings (global) and parameters (form and field rendering)


4.2.0 (2014-04-06)
++++++++++++++++++

* moved styling of form level errors to template
* bug fixes


4.1.1 (2014-04-06)
++++++++++++++++++

* moved all text conversions to text_value


4.1.0 (2014-04-05)
++++++++++++++++++

* typo fix and internal branching changes


4.0.3 (2014-04-03)
++++++++++++++++++

* fixed checkbox label bug in vertical and inline forms


4.0.2 (2014-04-02)
++++++++++++++++++

* fixed bug in vertical form rendering


4.0.1 (2014-03-29)
++++++++++++++++++

* fixed unicode bug and added unicode label to tests


4.0.0 (2014-03-28)
++++++++++++++++++

* use renderer classes for generating HTML
* several bug fixes


3.3.0 (2014-03-19)
++++++++++++++++++

* use Django forms css classes for indicating required and error on fields


3.2.1 (2014-03-16)
++++++++++++++++++

* improved form rendering


3.2.0 (2014-03-11)
++++++++++++++++++

* support for addons


3.1.0 (2014-03-03)
++++++++++++++++++

* improve compatibility with Django < 1.5


3.0.0 (2014-02-28)
++++++++++++++++++

* added support for themes (fix issue #74)
* show inline form errors in field title (fix issue #81)
* fixed bugs in demo application
* update to newest Bootstrap (fix issue #83)


2.6.0 (2014-02-20)
++++++++++++++++++

* new setting `set_required` to control setting of HTML `required` attribute (fix issue #76)


2.5.6 (2014-01-23)
++++++++++++++++++

* project refactored
* added skeleton for creating documentation (fix issue #30)
* fixed `FileField` issues



