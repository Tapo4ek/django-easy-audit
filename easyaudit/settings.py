# -*- coding: utf-8 -*-


from importlib import import_module

from django.apps.registry import apps
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.migrations import Migration
from django.db.migrations.recorder import MigrationRecorder
from django.utils import six

# default unregistered classes
UNREGISTERED_CLASSES = [Migration, LogEntry, Session, Permission, ContentType,
                        MigrationRecorder.Migration]

# override default unregistered classes if defined in project settings
UNREGISTERED_CLASSES = getattr(settings, 'DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_DEFAULT', UNREGISTERED_CLASSES)

# extra unregistered classes
UNREGISTERED_CLASSES.extend(getattr(settings, 'DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA', []))

UNREGISTERED_APPS = ['easyaudit']

# override default unregistered apps if defined in project settings
UNREGISTERED_APPS = getattr(settings, 'DJANGO_EASY_AUDIT_UNREGISTERED_APPS', UNREGISTERED_APPS)

# extra unregistered apps
UNREGISTERED_APPS.extend(getattr(settings, 'DJANGO_EASY_AUDIT_UNREGISTERED_APPS_EXTRA', []))

for app in UNREGISTERED_APPS:
    if isinstance(app, six.string_types):
        UNREGISTERED_CLASSES.extend(apps.get_app_config(app).get_models())

for idx, item in enumerate(UNREGISTERED_CLASSES):
    if isinstance(item, six.string_types):
        model_class = apps.get_model(item)
        UNREGISTERED_CLASSES[idx] = model_class

# should login events be registered?
WATCH_LOGIN_EVENTS = getattr(settings, 'DJANGO_EASY_AUDIT_WATCH_LOGIN_EVENTS', True)

# should model events be registered?
WATCH_MODEL_EVENTS = getattr(settings, 'DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS', True)

# should request events be registered?
WATCH_REQUEST_EVENTS = getattr(settings, 'DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS', True)

# Make records undeletable for all users
ALLOW_DELETE_RECORDS = getattr(settings, 'DJANGO_EASY_AUDIT_ALLOW_DELETE_RECORDS', True)

# Make records uneditable for all users
ALLOW_EDIT_RECORDS = getattr(settings, 'DJANGO_EASY_AUDIT_ALLOW_EDIT_RECORDS', True)

# Disallow add records for all users
ALLOW_ADD_REDORDS = getattr(settings, 'DJANGO_EASY_AUDIT_ALLOW_ADD_REDORDS', True)

WRITE_EVENTS_ONLY_LOGGED_IN_USERS = getattr(settings, 'DJANGO_EASY_AUDIT_WRITE_EVENTS_ONLY_LOGGED_IN_USERS', False)

# project defined callbacks
CRUD_DIFFERENCE_CALLBACKS = []
CRUD_DIFFERENCE_CALLBACKS = getattr(settings, 'DJANGO_EASY_AUDIT_CRUD_DIFFERENCE_CALLBACKS', CRUD_DIFFERENCE_CALLBACKS)
# the callbacks could come in as an iterable of strings, where each string is the package.module.function
for idx, callback in enumerate(CRUD_DIFFERENCE_CALLBACKS):
    if not callable(callback):  # keep as is if it is callable
        CRUD_DIFFERENCE_CALLBACKS[idx] = getattr(import_module('.'.join(callback.split('.')[:-1])),
                                                 callback.split('.')[-1], None)
