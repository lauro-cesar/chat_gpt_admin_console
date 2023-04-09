"""
Copyright (c) 2020, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
class OrganizationsConfig(AppConfig):
    name = "organizations"
    verbose_name = _("Organizations")

    def ready(self):
        import organizations.signals
