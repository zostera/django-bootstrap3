try:
    from django.utils.encoding import force_text as force_unicode
except ImportError:
    from django.utils.encoding import force_unicode


def force_text(s):
    if isinstance(s, str):
        return s
    return force_unicode(s)