from django import get_version

DJANGO3 = get_version() >= "3"


def html_39x27(html):
    """
    Return HTML string with &#x27; in stead of &#39;.

    See https://docs.djangoproject.com/en/dev/releases/3.0/#miscellaneous
    """
    if DJANGO3:
        return html.replace("&#39;", "&#x27;")
    return html
