======================
Bootstrap 3 for Django
======================

Write Django as usual, and let ``django-bootstrap3`` make template output into Bootstrap 3 code.


.. image:: https://img.shields.io/travis/dyve/django-bootstrap3/master.svg
    :target: https://travis-ci.org/dyve/django-bootstrap3

.. image:: https://img.shields.io/coveralls/dyve/django-bootstrap3/master.svg
  :target: https://coveralls.io/r/dyve/django-bootstrap3?branch=master

.. image:: https://img.shields.io/pypi/v/django-bootstrap3.svg
    :target: https://pypi.python.org/pypi/django-bootstrap3
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/django-bootstrap3.svg
    :target: https://pypi.python.org/pypi/django-bootstrap3
    :alt: Number of PyPI downloads per month


Requirements
------------

- Python 2.7, 3.2, 3.3, 3.4, or 3.5
- Django >= 1.8

*The latest version supporting Python 2.6 and Django < 1.8 is the 6.x.x branch.*


Installation
------------

1. Install using pip:

   ``pip install django-bootstrap3``

   Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to INSTALLED_APPS in your ``settings.py``:

   ``'bootstrap3',``

3. In your templates, load the ``bootstrap3`` library and use the ``bootstrap_*`` tags:

This app will soon require Django 1.8+, python 2.7+. Thanks for understanding.


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


Bugs and suggestions
--------------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/dyve/django-bootstrap3/issues


License
-------

You can use this under Apache 2.0. See `LICENSE
<LICENSE>`_ file for details.


Author
------

Developed and maintained by `Zostera <https://zostera.nl/>`_.

Original author & Development lead: `Dylan Verheul <https://github.com/dyve>`_.

Thanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.

Please see AUTHORS.rst for a list of contributors.
