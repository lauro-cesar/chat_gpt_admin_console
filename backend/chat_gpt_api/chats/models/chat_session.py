"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

import logging
logger = logging.getLogger(__name__)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from django.conf import settings
import base64
from django.urls import reverse
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from project.models import BaseModel, StackedModel


class ChatSession(BaseModel):
    MODEL_LIST_ORDER_VALUE = 0
    SERIALIZABLES =['id','session_questions','session_name','prompt']
    FLUTTER_TYPES = {
        "default": "String",
        "id": "int",
    }
    FLUTTER_MANY_TO_MANY = {}
    FLUTTER_ONE_TO_ONE = {}    
    READ_ONLY_FIELDS=['id','serial','session_questions']
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['label','rest_endpoint']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=[]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=[]
    EXCLUDE_FROM_ADMIN=[]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
    REST_BASENAME="chatsession"
 
    TASKS={
        'on_create':[],
        'on_save':[],
        'on_delete':[]
    }

    session_name = models.CharField(max_length=128,verbose_name=_("Nome da sessão"),help_text=_("Nome da sessão"))
    
    prompt = models.ForeignKey(
        "chats.Prompt",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name=_("ChatGPT prompt"),
        related_name="prompt_sessions"
    )




    @property
    def label(self):
        return "Sessao"

    class Meta(BaseModel.Meta):
        verbose_name = _("Sessao")
        verbose_name_plural = _("Sessões")

    def __str__(self):
        return self.label
