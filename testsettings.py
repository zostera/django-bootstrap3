import django.conf.global_settings as DEFAULT_SETTINGS


SECRET_KEY = 'bootstrap3isawesome'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'bootstrap3',
)

MIDDLEWARE_CLASSES = DEFAULT_SETTINGS.MIDDLEWARE_CLASSES

BOOTSTRAP3 = {
    'javascript_in_head': True,
    'required_css_class': 'bootstrap3-req',
    'error_css_class': 'bootstrap3-err',
    'success_css_class': 'bootstrap3-bound',
}
