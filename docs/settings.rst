========
Settings
========

The django-bootstrap3 has some pre-configured settings.

They can be modified by adding a dict variable called ``BOOTSTRAP3`` in your ``settings.py`` and customizing the values ​​you want;

The ``BOOTSTRAP3`` dict variable is configured by default to the following values​​:


.. code:: django

    # Default settings
    BOOTSTRAP3 = {
        'jquery_url': '//code.jquery.com/jquery.min.js',
        'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.1.1/',
        'css_url': None,
        'theme_url': None,
        'javascript_url': None,
        'javascript_in_head': False,
        'include_jquery': False,
        'horizontal_label_class': 'col-md-2',
        'horizontal_field_class': 'col-md-4',
        'set_required': True,
        'form_required_class': '',
        'form_error_class': '',
        'form_renderers': {
            'default': 'bootstrap3.renderers.FormRenderer',
        },
        'field_renderers': {
            'default': 'bootstrap3.renderers.FieldRenderer',
            'inline': 'bootstrap3.renderers.InlineFieldRenderer',
        },
    }
