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
from django.contrib import messages, admin
from project.models import BaseModel, StackedModel


class Prompt(BaseModel):
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
    ADMIN_LIST_DISPLAY=['label', 'organization','prompt_model','total_questions','rest_endpoint']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=["organization"]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=[]
    EXCLUDE_FROM_ADMIN=[]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
    REST_BASENAME="prompt"
 
    TASKS={
        'on_create':[],
        'on_save':[],
        'on_delete':[]
    }

    prompt_name = models.CharField(max_length=128,verbose_name=_("Nome do prompt"))
    prompt_model = models.CharField(max_length=512,verbose_name=_("Modelo"),default="gpt-3.5-turbo")
    prompt_command = models.TextField(verbose_name=_("Prompt do chat"), default="Eu sou uma bot altamente inteligente, sempre respondo com precisão. Se você me fizer uma pergunta relacionada com os conteúdos da base de conhecimento irei lhe responder. Mas se você fizer uma pergunta vaga ou a resposta não existir na base de conhecimento irei responder com: Não sei",)   
    prompt_temperature=models.FloatField(verbose_name=_("Nivel de randomização"),help_text=_("Usar valor entre 0 e 2."),default=0.3)
    prompt_max_tokens=models.PositiveSmallIntegerField(verbose_name=_("Máximo de tokens para a resposta"), default=100)
    prompt_frequency_penalty = models.IntegerField(verbose_name=_("Penalizar com base na frequencia de tokens"),default=0,help_text=_("Informar -0.2 até 0.2, quanto maior menor a probabilidade do chat repetir os tópicos"))
    prompt_presence_penalty = models.IntegerField(verbose_name=_("Penalizar com base na frequencia de tokens"),default=0, help_text=_("Informar -0.2 até 0.2, quanto maior menor a probabilidade do chat se repetir mesmas frases"))
    
    organization = models.ForeignKey(
        "organizations.Organization",
        related_name="organization_chats",
        verbose_name=_("Organização"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    @property
    @admin.display(description=_("Total de perguntas"))
    def total_questions(self):
        total =0 
        try:
            total =self.prompt_questions.count()
        except Exception as e:
            logger.error(e.__repr__())

        return total 
    
    @property
    def label(self):
        return  self.prompt_name

    class Meta(BaseModel.Meta):
        verbose_name = _("Prompts")
        verbose_name_plural = _("Prompts")

    def __str__(self):
        return self.label
