# django-bootstrap3 [![Build Status](https://secure.travis-ci.org/dyve/django-bootstrap3.png)](http://travis-ci.org/dyve/django-bootstrap3) [![PyPi version](https://pypip.in/v/django-bootstrap3/badge.png)](https://crate.io/packages/django-bootstrap3/) [![PyPi downloads](https://pypip.in/d/django-bootstrap3/badge.png)](https://crate.io/packages/django-bootstrap3/)


Bootstrap 3 integration with Django. Easily generate Bootstrap3 compatible HTML using template tags.


## Quick Start

1. Install using pip:

        pip install django-bootstrap3

   Alternatively, you can install download or clone this repo and call `pip install -e .`.

2. Add to INSTALLED_APPS in your `settings.py`:

        'bootstrap3',

3. In your templates, load the `bootstrap3` library and use the `bootstrap_*` tags

        {% load bootstrap3 %}
        
        {# Load CSS and JavaScript #}
        
        {% bootstrap_css %}
        {% bootstrap_javascript %}
        
        {# Display a form #}
        
        <form action="/url/to/submit/" method="post" class="form">
                {% csrf_token %}
                {% bootstrap_form form %}
                {% bootstrap_form_buttons %}
                        <button type="submit" class="btn btn-primary">
                                {% bootstrap_icon "star" %} Submit
                        </button>
                {% end_bootstrap_form_buttons %}
        </form>

## Requirements

- Python 2.6 or 2.7
- Django >= 1.4

Contributions and pull requests for other Django and Python versions are welcome.


## Bugs and requests

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/dyve/django-bootstrap3/issues


## License

You can use this under Apache 2.0. See LICENSE file for details.


## Author

My name is Dylan Verheul, you can reach me at <dylan@dyve.net> or [follow me on Twitter][1].




[1]: http://twitter.com/dyve
