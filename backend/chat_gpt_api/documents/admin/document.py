
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import ProjectBaseModelAdmin as BaseModelAdmin
from documents.models import Document
from project.admin import dashboard_sites, admin_sites
import numpy as np

class DocumentAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = Document.ADMIN_ORDERING
    list_display = Document.ADMIN_LIST_DISPLAY
    list_filter = Document.ADMIN_LIST_FILTER
    search_fields = Document.ADMIN_SEARCH_FILTER
    list_editable = Document.ADMIN_LIST_EDITABLE
    list_display_links=Document.ADMIN_DISPLAY_LINKS
    filter_horizontal= Document.ADMIN_FILTER_HORIZONTAL    
    exclude = list(np.unique([item for sublist in [BaseModelAdmin.exclude,Document.EXCLUDE_FROM_ADMIN] for item in sublist]))
    

    def has_delete_permission(self, request, obj=None):
        user = request.user
        checklist = []
        if hasattr(user, "is_rootuser"):
            checklist.append(user.is_rootuser)
        if hasattr(user, "is_superuser"):
            checklist.append(user.is_superuser)
        if hasattr(user, "is_operator"):
            checklist.append(user.is_operator)    
        
        if obj is not None:
            checklist.append(obj.criado_por in [user]) 
        return (True in checklist)


for admin_site in admin_sites:
    admin_site.register(Document,DocumentAdmin)


for developer_site in dashboard_sites:
    developer_site.register(Document,DocumentAdmin)
