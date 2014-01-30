=============================
django-bootstrap3
=============================

.. image:: https://travis-ci.org/dyve/django-bootstrap3.png?branch=master
    :target: https://travis-ci.org/dyve/django-bootstrap3

.. image:: https://badge.fury.io/py/django-bootstrap3.png
    :target: http://badge.fury.io/py/django-bootstrap3

.. image:: https://pypip.in/d/django-bootstrap3/badge.png
    :target: https://crate.io/packages/django-bootstrap3?version=latest

Bootstrap support for Django projects

Documentation
-------------

The full documentation is at http://django-bootstrap3.rtfd.org.

Quickstart
----------

1. Install using pip:

        pip install django-bootstrap3

   Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to INSTALLED_APPS in your ``settings.py``:

        'bootstrap3',

3. In your templates, load the ``bootstrap3`` library and use the ``bootstrap_*`` tags:

        {% load bootstrap3 %}
        
        {# Load CSS and JavaScript #}
        
        {% bootstrap_css %}
        {% bootstrap_javascript %}
        
        {# Display django.contrib.messages as Bootstrap alerts }
        {% bootstrap_messages %}

        {# Display a form #}
        
        <form action="/url/to/submit/" method="post" class="form">
            {% csrf_token %}
            {% bootstrap_form form %}
            {% buttons %}
                <button type="submit" class="btn btn-primary">
                    {% bootstrap_icon "star" %} Submit
                </button>
            {% endbuttons %}
        </form>



Features
--------

* TODO


Requirements
------------

- Python 2.6, 2.7 and 3.3
- Django >= 1.4

Contributions and pull requests for other Django and Python versions are welcome.


Bugs and requests
------------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/dyve/django-bootstrap3/issues


License
-------

You can use this under Apache 2.0. See LICENSE file for details.

Author
-------

My name is Dylan Verheul, you can reach me at <dylan@dyve.net> or [follow me on Twitter][1].


[1]: http://twitter.com/dyve

