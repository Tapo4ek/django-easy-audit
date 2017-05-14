# -*- coding: utf-8 -*-


from django.contrib import admin
from . import models
from . import settings


class PermissionsMixin(object):

    def has_delete_permission(self, request, obj=None):
        if settings.ALLOW_DELETE_RECORDS:
            return super(PermissionsMixin, self).has_delete_permission(request, obj=obj)
        return False

    def has_add_permission(self, request):
        if settings.ALLOW_ADD_REDORDS:
            return super(PermissionsMixin, self).has_add_permission(request)
        return False

    def get_readonly_fields(self, request, obj=None):
        if settings.ALLOW_EDIT_RECORDS:
            return super(PermissionsMixin, self).get_readonly_fields(request, obj=obj)
        return [f.name for f in self.model._meta.fields]


class CRUDEventAdmin(PermissionsMixin, admin.ModelAdmin):
    list_filter = ['event_type', 'content_type', 'user']
    list_display = ['event_type', 'content_type', 'object_id',
                    'object_repr', 'user', 'datetime']

admin.site.register(models.CRUDEvent, CRUDEventAdmin)


class LoginEventAdmin(PermissionsMixin, admin.ModelAdmin):
    list_display = ['datetime', 'get_login_type_display', 'username', 'user']


admin.site.register(models.LoginEvent, LoginEventAdmin)


class RequestEventAdmin(PermissionsMixin, admin.ModelAdmin):
    list_display = ['datetime', 'type', 'user', 'uri', 'remote_ip']
