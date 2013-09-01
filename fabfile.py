from __future__ import unicode_literals

import os, sys

from datetime import datetime

from fabric.api import local, run, env
from fabric.context_managers import cd
from fabric.contrib import django


project = 'animaltrack'

zi_user = project
zp_user = project
app_name = project
django_settings = 'app.settings'


# Fix path
FABFILE_DIR = os.path.dirname(__file__)
sys.path.append(FABFILE_DIR)

# Integrate Django project
django.settings_module(django_settings)

# Load Django settings
from django.conf import settings


def zi():
    # Set host to zi
    env.hosts = ['%s@zi.zostera.nl' % zi_user]


def zp():
    # Set host to zp
    env.hosts = ['%s@zp.zostera.nl' % zp_user]


def upgrade():
    # Update all pip packages
    local("pip freeze |sed -ne 's/==.*//p' |xargs pip install -U --")
    requirements()


def requirements():
    # Update requirements.txt, skip readline
    local("pip freeze | grep -v readline > requirements.txt")


def translate():
    # Make translation files
    for lang, language in settings.LANGUAGES:
        if lang != 'en':
            local("python manage.py makemessages -l %s" % lang)
            local("python manage.py makemessages -d djangojs -l %s" % lang)


def update():
    # Perform local tasks to update the environment
    requirements()
    translate()


def restart():
    # Restart Django app
    run('/usr/bin/sudo /usr/bin/supervisorctl restart %s' % app_name)


def deploy():
    # Deploy Django app
    tag()
    with cd('~/django'):
        run('git pull origin master')
        run('pip install -r requirements.txt')
        run('python manage.py syncdb')
        run('python manage.py migrate')
        run('python manage.py collectstatic --noinput')
    restart()


def delete_stale_content_types():
    # Delete stale content types, South and syncdb sometimes mess up
    from django.contrib.contenttypes.models import ContentType
    for c in ContentType.objects.all():
        if not c.model_class():
            print "Deleting %s" % c
            c.delete()

def tag():
    # Tag current source for deploy
    host = env.hosts[0]
    parts = host.split('@')[1]
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    tag = parts.split('.')[0] + timestamp
    msg = 'Deploy to %s on %s' % (host, timestamp)
    local("git tag -a %s -m '%s'" % (tag, msg))