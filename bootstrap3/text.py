from django.utils.encoding import force_text


def text_value(value):
    """Force a value to text, render None as an empty string."""
    if value is None:
        return ""
    return force_text(value)


def text_concat(*args, **kwargs):
    """Concatenate several values as a text string with an optional separator."""
    separator = text_value(kwargs.get("separator", ""))
    values = filter(None, [text_value(v) for v in args])
    return separator.join(values)
