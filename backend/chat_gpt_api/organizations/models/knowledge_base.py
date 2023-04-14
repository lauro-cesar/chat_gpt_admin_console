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
from django.utils.text import slugify


class KnowledgeBase(BaseModel):
    MODEL_LIST_ORDER_VALUE = 0
    SERIALIZABLES =['id','organization','knowledge_base_name']
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
    ADMIN_LIST_FILTER=["organization"]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=[]
    EXCLUDE_FROM_ADMIN=[]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
    REST_BASENAME="knowledgebase"
 
    TASKS={
        'on_create':["create_redis_index"],
        'on_save':[],
        'on_delete':[]
    }

    # Redis index created using: self.knowledge_base_name + self.id
    knowledge_base_name = models.CharField(max_length=512,verbose_name=_("Nome da base de conhecimento"),help_text=_("Utilizado na criação do indice"))    
    organization = models.ForeignKey(
        "organizations.Organization",
        related_name="organization_knowledge_base_collection",
        verbose_name=_("Organização"),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    @property
    def vector_prefix(self):
        """ 
        """
        return f"docs_for_{slugify(self.knowledge_base_name)}"

    @property
    def vector_index_name(self):
        """
        """
        return f"embeddings-index-{self.id}_HNSW"
 


    @property
    def label(self):
        return  self.knowledge_base_name


    class Meta(BaseModel.Meta):
        verbose_name = _("Base de conhecimento")
        verbose_name_plural = _("Bases de conhecimentos")

    def __str__(self):
        return self.label
