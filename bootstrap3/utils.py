from __future__ import absolute_import
from __future__ import unicode_literals


try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
