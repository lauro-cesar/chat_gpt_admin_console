
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
from chats.models import Question
from project.admin import dashboard_sites, admin_sites
import numpy as np

class QuestionAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = Question.ADMIN_ORDERING
    list_display = Question.ADMIN_LIST_DISPLAY
    list_filter = Question.ADMIN_LIST_FILTER
    search_fields = Question.ADMIN_SEARCH_FILTER
    list_editable = Question.ADMIN_LIST_EDITABLE
    list_display_links=Question.ADMIN_DISPLAY_LINKS
    filter_horizontal= Question.ADMIN_FILTER_HORIZONTAL    
    exclude = list(np.unique([item for sublist in [BaseModelAdmin.exclude,Question.EXCLUDE_FROM_ADMIN] for item in sublist]))
    

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
    admin_site.register(Question,QuestionAdmin)


for developer_site in dashboard_sites:
    developer_site.register(Question,QuestionAdmin)
