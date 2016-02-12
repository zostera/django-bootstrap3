import django.conf.global_settings as DEFAULT_SETTINGS

SECRET_KEY = 'bootstrap3isawesome'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # We test this one
    'bootstrap3',
)

MIDDLEWARE_CLASSES = DEFAULT_SETTINGS.MIDDLEWARE_CLASSES

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
}]

ROOT_URLCONF = None

BOOTSTRAP3 = {
    'javascript_in_head': True,
    'required_css_class': 'bootstrap3-req',
    'error_css_class': 'bootstrap3-err',
    'success_css_class': 'bootstrap3-bound',
}
