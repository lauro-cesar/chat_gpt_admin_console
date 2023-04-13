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
from project.models import BaseModel, StackedModel,BaseModelForeignMixin


class Embedding(BaseModel,BaseModelForeignMixin):
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
    ADMIN_LIST_DISPLAY=['label','document_page','isIndexed','inProgress','isReadyForIndex','num_tokens','hasErrors','rest_endpoint']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=["document__organization","hasErrors",'isIndexed','inProgress','isReadyForIndex']
    ADMIN_SEARCH_FILTER=["document__document_file"]
    ADMIN_DISPLAY_LINKS=[]
    EXCLUDE_FROM_ADMIN=["isIndexed","inProgress"]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
    REST_BASENAME="embedding"
 
    TASKS={
        'on_create':[],
        'on_save':["create_embedding_index"],
        'on_delete':[]
    }

    hasErrors = models.BooleanField(default=False)
    lastLog = models.JSONField(default=dict, blank=True,null=True)
    isIndexed = models.BooleanField(default=False)
    inProgress = models.BooleanField(default=False)
    isReadyForIndex = models.BooleanField(default=False)
    embedding_raw_content = models.TextField()
    generated_embedding = models.JSONField(default=dict)
    num_tokens = models.PositiveSmallIntegerField(default=0,verbose_name=_("Total de tokens"))
    document_page = models.PositiveSmallIntegerField(verbose_name=_("Página correspondente"),default=1)
    
    document = models.ForeignKey(
        "documents.Document",
        related_name="document_embeddings",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Documento")
    )


    @property
    def label(self):
        document_name = ""
        try:
            document_name = self.document.label
        except Exception as e:
            logger.error(e.__repr__())
        return  document_name

    class Meta(BaseModel.Meta):
        verbose_name = _("Raw embedding chunk")
        verbose_name_plural = _("Raw embeddings chunks")

    def __str__(self):
        return self.label
