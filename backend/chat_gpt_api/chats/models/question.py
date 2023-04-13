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
from django.contrib import messages,admin
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
    ADMIN_LIST_DISPLAY=['label','resposta','question_content','isReadyToAsk','isReady','hasErrors','rest_endpoint']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=["prompt__organization",'isReadyToAsk','isReady','hasErrors']
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=[]
    EXCLUDE_FROM_ADMIN=["generated_embedding","isReady","num_tokens","lastLog"]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
    REST_BASENAME="question"
 
    TASKS={
        'on_create':["prepare_question"],
        'on_save':["prepare_question"],
        'on_delete':[]
    }

    question_content = models.TextField(verbose_name=_("Pergunta"))
    generated_embedding = models.JSONField(default=dict,        blank=True,
        null=True)


    @property
    def embedded_query(self):
        query = None 
        try:
            query = self.generated_embedding.get("data",{})[0].get("embedding")
        except Exception as e:
            return None 
    
        return query
    

    num_tokens = models.PositiveSmallIntegerField(default=0,verbose_name=_("Total de tokens"))
    isReady = models.BooleanField(default=False)
    isReadyToAsk = models.BooleanField(default=False)
    hasErrors = models.BooleanField(default=False)
    lastLog = models.JSONField(default=dict,blank=True,null=True)

    answer = models.ForeignKey(
        "chats.Answer",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Resposta"),
        related_name="questions_using_this_answer"
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
    @admin.display(description="Resposta")
    def resposta(self): 
        try:
            answer_content = self.answer.answer_content
        except Exception as e:
            answer_content = "Aguardando resposta"

        return mark_safe(f"<textarea>{answer_content}</textarea>")
    
    @property
    def label(self):
        return self.question_content

    class Meta(BaseModel.Meta):
        verbose_name = _("Pergunta")
        verbose_name_plural = _("Perguntas")

    def __str__(self):
        return self.label
