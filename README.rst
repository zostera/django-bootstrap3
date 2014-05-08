============================
Welcome to django-bootstrap3
============================

.. image:: https://travis-ci.org/dyve/django-bootstrap3.png?branch=master
    :target: https://travis-ci.org/dyve/django-bootstrap3

.. image:: https://badge.fury.io/py/django-bootstrap3.png
    :target: http://badge.fury.io/py/django-bootstrap3

.. image:: https://pypip.in/d/django-bootstrap3/badge.png
    :target: https://crate.io/packages/django-bootstrap3?version=latest


Use Bootstrap in your Django templates, the Django way.


Installation
------------

1. Install using pip:

   ``pip install django-bootstrap3``

   Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to INSTALLED_APPS in your ``settings.py``:

   ``'bootstrap3',``

3. In your templates, load the ``bootstrap3`` library and use the ``bootstrap_*`` tags:


Example template
----------------

   .. code:: Django

    {% load bootstrap3 %}

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


Documentation
-------------

The full documentation is at http://django-bootstrap3.readthedocs.org/.


Requirements
------------

- Python 2.6, 2.7, 3.2 or 3.3
- Django >= 1.4

Contributions and pull requests for other Django and Python versions are welcome.


Bugs and requests
-----------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/dyve/django-bootstrap3/issues


License
-------

You can use this under Apache 2.0. See `LICENSE
<LICENSE>`_ file for details.


Author
------

My name is Dylan Verheul, you can reach me at dylan@dyve.net or follow me on Twitter (http://twitter.com/dyve). If you like this project, you can `support me on GitTip <https://www.gittip.com/dyve/>`_.
