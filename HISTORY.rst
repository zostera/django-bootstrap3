.. :changelog:

History
-------


5.0.1 (2014-11-21)
++++++++++++++++++

* Bug fixes and update to Bootstrap 3.2.1


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



