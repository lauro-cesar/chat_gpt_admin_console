
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

import logging
logger = logging.getLogger(__name__)
from celery import shared_task
from django.conf import settings
from django.utils.encoding import smart_str
from PIL import Image, ImageOps, ImageDraw,ImageFont
from io import BytesIO
from django.core.cache import cache
from django.utils.text import slugify
import json
from django.urls import reverse_lazy
import base64
from project.celery_tasks import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from organizations.models import KnowledgeBase
from organizations.serializers import KnowledgeBaseSerializer, KnowledgeBaseIdOnlySerializer
import tiktoken
import openai
import redis
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)
from redis.commands.search.query import Query
from redis.commands.search.field import (
    TextField,
    VectorField
)
import os


redis_client = redis.Redis(
    password=settings.REDIS_VECTOR_DB_PASSWORD,
    port=settings.REDIS_VECTOR_DB_PORT,
    host=settings.REDIS_VECTOR_DB_HOST
)


@shared_task(name="create_redis_index", max_retries=2, soft_time_limit=45)
def on_create_redis_index_task(object_pk):
    instance = KnowledgeBase.get_or_none(pk=object_pk)
    if instance:
        logger.info(f"Creating index for: {instance.vector_index_name}")

        embedding_raw_content = TextField(name="embedding_raw_content")

        generated_embedding = VectorField("generated_embedding",
        "HNSW", {
            "TYPE": "FLOAT32",
            "DIM": settings.VECTOR_DB_VECTOR_DIM,
            "DISTANCE_METRIC": settings.VECTOR_DB_DISTANCE_METRIC,
            "INITIAL_CAP": settings.VECTOR_DB_VECTOR_NUMBER
        }
        )

        fields = [embedding_raw_content, generated_embedding]

        try:       
            redis_client.ft(instance.vector_index_name).info()
        except Exception as e:    
            redis_client.ft(instance.vector_index_name).create_index(fields=fields,definition=IndexDefinition(prefix=[instance.vector_prefix],index_type=IndexType.HASH))
        



@shared_task(name="organizations_collection_id_only_knowledgebase", max_retries=2, soft_time_limit=45)
def on_organizations_collection_id_only_knowledgebase_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = KnowledgeBase.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = KnowledgeBaseIdOnlySerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"organizations_collection_id_only_knowledgebase", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")
        
        
@shared_task(name="organizations_collection_knowledgebase", max_retries=2, soft_time_limit=45)
def on_organizations_collection_id_only_knowledgebase_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = KnowledgeBase.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = KnowledgeBaseSerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"organizations_collection_knowledgebase", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")



@shared_task(name="stream_live_update_knowledgebase", max_retries=2, soft_time_limit=45)
def on_stream_live_update_knowledgebase_task(object_pk):
    instance = KnowledgeBase.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = KnowledgeBaseSerializer(instance)
            async_to_sync(channel_layer.group_send)(
                f"KnowledgeBase_{object_pk}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())  