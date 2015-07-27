from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


def format_html_pre_18(format_string, *args, **kwargs):
    """
    Fake function to support format_html in Django < 1.8
    """
    args_safe = map(conditional_escape, args)
    kwargs_safe = {}
    for k in kwargs:
        kwargs_safe[k] = conditional_escape(kwargs[k])
    return mark_safe(format_string.format(*args_safe, **kwargs_safe))
