# -*- coding: utf-8 -*-


from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EasyAuditConfig(AppConfig):
    name = 'easyaudit'
    verbose_name = _('Easy Audit Application')

    def ready(self):
        import easyaudit.signals
