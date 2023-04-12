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


class Question(BaseModel):
    MODEL_LIST_ORDER_VALUE = 0
    SERIALIZABLES =['id','label','serial']
    FLUTTER_TYPES = {
        "default": "String",
        "id": "int",
    }
    FLUTTER_MANY_TO_MANY = {}
    FLUTTER_ONE_TO_ONE = {}    
    READ_ONLY_FIELDS=['id','serial']
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['label','rest_endpoint']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=["prompt__organization"]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=[]
    EXCLUDE_FROM_ADMIN=["answer"]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
    REST_BASENAME="question"
 
    TASKS={
        'on_create':[],
        'on_save':[],
        'on_delete':[]
    }

    question_content = models.TextField(verbose_name=_("Pergunta"))

    answer = models.ForeignKey(
        "chats.Answer",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Resposta"),
        related_name="answer_questions"
    )

    prompt = models.ForeignKey(
        "chats.Prompt",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("ChatGPT prompt"),
        related_name="prompt_questions"
    )


    @property
    def label(self):
        return self.question_content

    class Meta(BaseModel.Meta):
        verbose_name = _("Pergunta")
        verbose_name_plural = _("Perguntas")

    def __str__(self):
        return self.label
