.. code:: django

  {# Load the tag library #}
  {% load bootstrap3 %}

  {# Load CSS and JavaScript #}
  {% bootstrap_css %}
  {% bootstrap_javascript %}

  {# Display django.contrib.messages as Bootstrap alerts #}
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

  {# Read the documentation for more information #}
