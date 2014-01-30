========================
Template tags and Usage
========================


1. Add to INSTALLED_APPS in your ``settings.py``:

::

        'bootstrap3',

2. In your templates, load the ``bootstrap3`` library and use the ``bootstrap_*`` tags:

::

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

**The ``bootstrap3`` template tag library includes the following template tags:**

.. note::

 All the following examples it is understood that you have already loaded the ``bootstrap3`` 
 template tag library, placing the code below in the beginning that each template that ``bootstrap3`` 
 template tag library will be used:

  ::

  {% load bootstrap3 %}


bootstrap_form
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_form


bootstrap_formset
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_formset


bootstrap_field
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_field


bootstrap_label
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_label



bootstrap_button
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_button


bootstrap_icon
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_icon


buttons
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_buttons


bootstrap_messages
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_messages


bootstrap_pagination
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_pagination



bootstrap_jquery_url
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_jquery_url



bootstrap_javascript_url
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_javascript_url


bootstrap_css_url
~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_css_url



bootstrap_css
~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_css


bootstrap_javascript
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bootstrap3.templatetags.bootstrap3.bootstrap_javascript


