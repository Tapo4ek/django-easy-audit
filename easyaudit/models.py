# -*- coding: utf-8 -*-


from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseEventModel(models.Model):
    """All fields are required in every event models"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), null=True, blank=True,
                             on_delete=models.SET_NULL)
    datetime = models.DateTimeField(_('Datetime'), auto_now_add=True)

    class Meta:
        abstract = True


class CRUDEvent(BaseEventModel):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
    TYPES = (
        (CREATE, _('Create')),
        (UPDATE, _('Update')),
        (DELETE, _('Delete')),
    )

    event_type = models.SmallIntegerField(_('Event type'), choices=TYPES)
    object_id = models.IntegerField(_('Object id'))  # we should try to allow other ID types
    content_type = models.ForeignKey(ContentType, verbose_name=_('Model'))
    object_repr = models.CharField(_('Object'), max_length=255, null=True, blank=True)
    object_json_repr = models.TextField(_('Object json'), null=True, blank=True)
    user_pk_as_string = models.CharField(_('User identifier'), max_length=255, null=True, blank=True,
                                         help_text=_('String version of the user pk'))
    remote_ip = models.CharField(_('Remote IP'), max_length=20, null=True, db_index=True)

    def is_create(self):
        return self.CREATE == self.event_type

    def is_update(self):
        return self.UPDATE == self.event_type

    def is_delete(self):
        return self.DELETE == self.event_type

    class Meta:
        verbose_name = _('CRUD event')
        verbose_name_plural = _('CRUD events')
        ordering = ['-datetime']


class LoginEvent(BaseEventModel):
    LOGIN = 0
    LOGOUT = 1
    FAILED = 2
    TYPES = (
        (LOGIN, _('Login')),
        (LOGOUT, _('Logout')),
        (FAILED, _('Failed login')),
    )
    login_type = models.SmallIntegerField(_('Login type'), choices=TYPES)
    username = models.CharField(_('Username'), max_length=255, null=True, blank=True)
    remote_ip = models.CharField(_('Remote IP'), max_length=20, null=True, db_index=True)

    class Meta:
        verbose_name = _('Login event')
        verbose_name_plural = _('Login events')
        ordering = ['-datetime']


class RequestEvent(BaseEventModel):
    uri = models.CharField(_('Uri'), max_length=255, null=False, db_index=True)
    type = models.CharField(_('Type'), max_length=20, null=False, db_index=True)
    query_string = models.CharField(_('Query string'), max_length=255, null=True)
    remote_ip = models.CharField(_('Remote IP'), max_length=20, null=False, db_index=True)

    class Meta:
        verbose_name = _('Request event')
        verbose_name_plural = _('Request events')
        ordering = ['-datetime']
