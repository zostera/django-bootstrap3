# django-bootstrap3 [![Build Status](https://secure.travis-ci.org/dyve/django-bootstrap3.png)](http://travis-ci.org/dyve/django-bootstrap3)


**Bootstrap 3 integration with Django.**

**Author:** Dylan Verheul, <dylan@dyve.net> ([Follow me on Twitter][1]).


## Installation

1. Install using pip:

        pip install django-bootstrap3

2. Add to INSTALLED_APPS:

        'bootstrap_3',

Alternatively, you can download or clone this repo and call `pip install -e .`.


## Usage

In your templates, load the `bootstrap3` library and use the `bootstrap_*` tags

    {% load bootstrap3 %}

    <form action="/url/to/submit/" method="post" class="form">
        {% csrf_token %}
        {% bootstrap_form form %}
        {% bootstrap_form_buttons %}
            <button type="submit" class="btn btn-primary">Submit</button>
        {% end_bootstrap_form_buttons %}
    </form>


## Bugs and requests

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/dyve/django-bootstrap3/issues


## License

You can use this under Apache 2.0. See LICENSE file for details.


[1]: http://twitter.com/dyve
