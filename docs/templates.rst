=========
Templates
=========

You can customize the output of ``django-bootstrap3`` by writing your own templates. These templates are available:


bootstrap3/field_help_text_and_errors.html
------------------------------------------

This renders the help text and error of each field.

Variable ``help_text_and_errors`` contains an array of strings.


bootstrap3/form_errors.html
---------------------------

This renders the non field errors of a form.

Variable ``errors`` contains an array of strings.


bootstrap3/messages.html
------------------------

This renders the Django messages variable.

Variable ``messages`` contains the messages as described in https://docs.djangoproject.com/en/dev/ref/contrib/messages/#displaying-messages


Other
-----

There are two more templates, ``bootstrap3/bootstrap3.html`` and ``bootstrap3/pagination.html``. You should consider these private for now, meaning you can use them but not modify them.
