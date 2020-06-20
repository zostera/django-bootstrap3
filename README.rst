======================
Bootstrap 3 for Django
======================

.. image:: https://travis-ci.org/zostera/django-bootstrap3.svg
    :target: https://travis-ci.org/zostera/django-bootstrap3

.. image:: https://readthedocs.org/projects/django-bootstrap3/badge/?version=latest
    :target: https://django-bootstrap3.readthedocs.io/en/latest/

.. image:: https://img.shields.io/pypi/v/django-bootstrap3.svg
    :target: https://pypi.org/project/django-bootstrap3/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. image:: https://coveralls.io/repos/github/zostera/django-bootstrap3/badge.svg
    :target: https://coveralls.io/r/zostera/django-bootstrap3


Bootstrap 3 integration for Django.

Goal
----

The goal of this project is to seamlessly blend Django and Bootstrap 3.

**Want to use Bootstrap 4 in Django?**

See https://github.com/zostera/django-bootstrap4.


Requirements
------------

- Python >= 3.5, Django >= 2.1 (see also https://docs.djangoproject.com/en/dev/faq/install/#faq-python-version-support)

Need older versions?
++++++++++++++++++++

- Version 11.x.x can be used for Python 2.7.x with Django 1.11, but you are encouraged to upgrade.

If you need even older versions, this is our history of dropping support for Python and Django versions. Note that this information is "as is", and you should really update to newer Python and Django versions. Using unsupported versions will lead to security risks and broken software.

- *The latest version supporting Django 2.0 is 11.x.x.*
- *The latest version supporting Django < 1.11 is 9.x.x.*
- *The latest version supporting Python 2.6 and Django < 1.8 is 6.x.x.*


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

The full documentation is at https://django-bootstrap3.readthedocs.org/.


Bugs and suggestions
--------------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/dyve/django-bootstrap3/issues


License
-------

You can use this under BSD-3-Clause. See `LICENSE <LICENSE>`_ file for details.


Author
------

Developed and maintained by `Zostera <https://zostera.nl/>`_.

Original author & Development lead: `Dylan Verheul <https://github.com/dyve>`_.

Thanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.

Please see `AUTHORS.rst <AUTHORS.rst>`_ for a list of contributors.
