"""Application configuration and system checks."""

from django.apps import AppConfig
from django.core.checks import Warning, register

#: Settings that existed once, with the hint that makes this worth more than "unknown key".
REMOVED_SETTINGS = {
    "base_url": "removed in 11.0.0, use `css_url` and `javascript_url`",
    "set_required": "removed in 11.0.0",
    "set_disabled": "removed in 11.0.0",
}


@register()
def check_bootstrap3_settings(app_configs, **kwargs):
    """Warn about keys in the BOOTSTRAP3 setting that this package never reads."""
    from django.conf import settings

    from bootstrap3.bootstrap import BOOTSTRAP3_DEFAULTS

    warnings = []
    for key in getattr(settings, "BOOTSTRAP3", {}):
        if key in BOOTSTRAP3_DEFAULTS:
            continue
        hint = REMOVED_SETTINGS.get(key, "not a django-bootstrap3 setting; it is ignored")
        warnings.append(
            Warning(
                f"BOOTSTRAP3[{key!r}] has no effect: {hint}.",
                id="bootstrap3.W001",
            )
        )
    return warnings


class Bootstrap3Config(AppConfig):
    """Default application configuration."""

    name = "bootstrap3"
