========
Settings
========

The django-bootstrap3 has some pre-configured settings.

They can be modified by adding a dict variable called ``BOOTSTRAP3`` in your ``settings.py`` and customizing the values ​​you want;

The ``BOOTSTRAP3`` dict variable contains these settings and defaults:


.. code:: django

    # Default settings
    BOOTSTRAP3 = {

        # The URL to the jQuery JavaScript file
        'jquery_url': '//code.jquery.com/jquery.min.js',

        # The Bootstrap base URL
        'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/',

        # The complete URL to the Bootstrap CSS file (None means derive it from base_url)
        'css_url': None,

        # The complete URL to the Bootstrap CSS file (None means no theme)
        'theme_url': None,

        # The complete URL to the Bootstrap JavaScript file (None means derive it from base_url)
        'javascript_url': None,

        # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap3.html)
        'javascript_in_head': False,

        # Include jQuery with Bootstrap JavaScript (affects django-bootstrap3 template tags)
        'include_jquery': False,

        # Label class to use in horizontal forms
        'horizontal_label_class': 'col-md-3',

        # Field class to use in horizontal forms
        'horizontal_field_class': 'col-md-9',

        # Set placeholder attributes to label if no placeholder is provided
        'set_placeholder': True,

        # Class to indicate required (better to set this in your Django form)
        'required_css_class': '',

        # Class to indicate error (better to set this in your Django form)
        'error_css_class': 'has-error',

        # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
        'success_css_class': 'has-success',

        # Renderers (only set these if you have studied the source and understand the inner workings)
        'formset_renderers':{
            'default': 'bootstrap3.renderers.FormsetRenderer',
        },
        'form_renderers': {
            'default': 'bootstrap3.renderers.FormRenderer',
        },
        'field_renderers': {
            'default': 'bootstrap3.renderers.FieldRenderer',
            'inline': 'bootstrap3.renderers.InlineFieldRenderer',
        },
    }
