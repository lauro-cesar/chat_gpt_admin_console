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
from project.models import BaseModel, StackedModel,BaseModelForeignMixin


class Document(BaseModel,BaseModelForeignMixin):
    MODEL_LIST_ORDER_VALUE = 0
    SERIALIZABLES =['id','document_file','knowledge_base']
    FLUTTER_TYPES = {
        "default": "String",
        "id": "int",
    }
    FLUTTER_MANY_TO_MANY = {}
    FLUTTER_ONE_TO_ONE = {}    
    READ_ONLY_FIELDS=['id','serial']
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['label','num_tokens','isIndexed','inProgress','rest_endpoint','vector_prefix','vector_index_name']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=["knowledge_base__organization"]
    ADMIN_SEARCH_FILTER=["document_file"]
    ADMIN_DISPLAY_LINKS=[]
    EXCLUDE_FROM_ADMIN=["num_tokens","metadata",'isIndexed','inProgress']
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
    REST_BASENAME="document"
 
    TASKS={
        'on_create':["extract_raw_embedding"],
        'on_save':[],
        'on_delete':[]
    }

    isIndexed = models.BooleanField(default=False)
    inProgress = models.BooleanField(default=False)
    document_file = models.FileField(verbose_name=_("Documento anexado"),blank=False,null=False)    
    metadata = models.JSONField(default=dict,blank=True,null=True)

    @property
    def vector_prefix(self):
        prefix = f"{self.id}"
        try:
            prefix = self.knowledge_base.vector_prefix
        except Exception as e:
            logger.error(e.__repr__())
    
        return prefix
    

    @property
    def vector_index_name(self):
        index_name = ""
        try:
            index_name = self.knowledge_base.vector_index_name
        except Exception as e:
            logger.error(e.__repr__())    
        return index_name
    

    @property
    @admin.display(description=_("Total de tokens no documento"))
    def num_tokens(self):   
        total = 0
        try:
            total = sum(list(map( lambda x:x.num_tokens,self.document_embeddings.all())))
        except Exception as e:
            logger.error(e.__repr__()) 
        return total
    
    knowledge_base = models.ForeignKey(
        "organizations.KnowledgeBase",
        related_name="organization_knowledge_base_docs",
        verbose_name=_("Base de conhecimento"),
        blank=False,
        null=False,
        on_delete=models.DO_NOTHING
    )


    @property
    def label(self):
        return  f"{self.document_file.name}"

    class Meta(BaseModel.Meta):
        verbose_name = _("Documento")
        verbose_name_plural = _("Documentos")

    def __str__(self):
        return self.label
