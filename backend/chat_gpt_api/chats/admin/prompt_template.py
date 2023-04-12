
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
from chats.models import PromptTemplate
from project.admin import dashboard_sites, admin_sites
import numpy as np

class PromptTemplateAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = PromptTemplate.ADMIN_ORDERING
    list_display = PromptTemplate.ADMIN_LIST_DISPLAY
    list_filter = PromptTemplate.ADMIN_LIST_FILTER
    search_fields = PromptTemplate.ADMIN_SEARCH_FILTER
    list_editable = PromptTemplate.ADMIN_LIST_EDITABLE
    list_display_links=PromptTemplate.ADMIN_DISPLAY_LINKS
    filter_horizontal= PromptTemplate.ADMIN_FILTER_HORIZONTAL    
    exclude = list(np.unique([item for sublist in [BaseModelAdmin.exclude,PromptTemplate.EXCLUDE_FROM_ADMIN] for item in sublist]))
    

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
            if hasattr(obj,"criado_por"):
                checklist.append(obj.criado_por in [user]) 
        return (True in checklist)


for admin_site in admin_sites:
    admin_site.register(PromptTemplate,PromptTemplateAdmin)


for developer_site in dashboard_sites:
    developer_site.register(PromptTemplate,PromptTemplateAdmin)
