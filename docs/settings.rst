========
Settings
========

The django-bootstrap3 has some pre-configured settings.

They can be modified by adding a dict variable called ``BOOTSTRAP3`` in your ``settings.py`` and customizing the values ​​you want;

The ``BOOTSTRAP3`` dict variable contains these settings and defaults:


.. code:: django

    # Default settings
    BOOTSTRAP3 = {

        # The complete URL to the Bootstrap CSS file
        # Note that a URL can be either
        # - a string, e.g. "//code.jquery.com/jquery.min.js"
        # - a dict like the default value below (use key "url" for the actual link)
        "css_url": {
            "url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
            "integrity": "sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u",
            "crossorigin": "anonymous",
        },

        # The complete URL to the Bootstrap CSS file (None means no theme)
        "theme_url": None,

        # The complete URL to the Bootstrap JavaScript file
        "javascript_url": {
            "url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js",
            "integrity": "sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa",
            "crossorigin": "anonymous",
        },

        # The URL to the jQuery JavaScript file
        "jquery_url": "//code.jquery.com/jquery.min.js",

        # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap3.html)
        "javascript_in_head": False,

        # Include jQuery with Bootstrap JavaScript (affects django-bootstrap3 template tags)
        "include_jquery": False,

        # Label class to use in horizontal forms
        "horizontal_label_class": "col-md-3",

        # Field class to use in horizontal forms
        "horizontal_field_class": "col-md-9",

        # Set HTML required attribute on required fields, for Django <= 1.8 only
        "set_required": True,

        # Set HTML disabled attribute on disabled fields, for Django <= 1.8 only
        "set_disabled": False,

        # Set placeholder attributes to label if no placeholder is provided.
        # This also considers the "label" option of {% bootstrap_field %} tags.
        "set_placeholder": True,

        # Class to indicate required (better to set this in your Django form)
        "required_css_class": "",

        # Class to indicate error (better to set this in your Django form)
        "error_css_class": "has-error",

        # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
        "success_css_class": "has-success",

        # Renderers (only set these if you have studied the source and understand the inner workings)
        "formset_renderers":{
            "default": "bootstrap3.renderers.FormsetRenderer",
        },
        "form_renderers": {
            "default": "bootstrap3.renderers.FormRenderer",
        },
        "field_renderers": {
            "default": "bootstrap3.renderers.FieldRenderer",
            "inline": "bootstrap3.renderers.InlineFieldRenderer",
        },
    }
