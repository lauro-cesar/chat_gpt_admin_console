
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
    actions=["prepare_question","retrieve_answer"]

    def retrieve_answer(self, request, queryset):
        for obj in queryset:
            try:
                result =  app.send_task("retrieve_answer",[obj.id])
            except Exception as e:
                self.message_user(
                    request,
                    f"{obj.label}: {e.__repr__()}",
                    messages.ERROR,
                )
            else:
                self.message_user(
                    request,
                    "{label}: enviado para a fila de processamento".format(label=obj),
                    messages.SUCCESS,
                )

    retrieve_answer.short_description = _("Executa o prompt")
    retrieve_answer.allowed_permissions = ['retrieve_answer']

    def has_retrieve_answer_permission(self,request, obj=None):
        return request.user.is_superuser  
    



    def prepare_question(self, request, queryset):
        for obj in queryset:
            try:
                result =  app.send_task("prepare_question",[obj.id])
            except Exception as e:
                self.message_user(
                    request,
                    f"{obj.label}: {e.__repr__()}",
                    messages.ERROR,
                )
            else:
                self.message_user(
                    request,
                    "{label}: enviado para a fila de processamento".format(label=obj),
                    messages.SUCCESS,
                )

    prepare_question.short_description = _("Prepara a pergunta")
    prepare_question.allowed_permissions = ['prepare_question']

    def has_prepare_question_permission(self,request, obj=None):
        return request.user.is_superuser  
    

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
    admin_site.register(Question,QuestionAdmin)


for developer_site in dashboard_sites:
    developer_site.register(Question,QuestionAdmin)
