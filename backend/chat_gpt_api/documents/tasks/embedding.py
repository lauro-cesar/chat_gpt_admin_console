
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
from documents.models import Embedding
from documents.serializers import EmbeddingSerializer, EmbeddingIdOnlySerializer

from project.indexador import IndexadorDeDocumentos
import tiktoken
import openai
import redis
import numpy as np



redis_client = redis.Redis(
    password=settings.REDIS_VECTOR_DB_PASSWORD,
    port=settings.REDIS_VECTOR_DB_PORT,
    host=settings.REDIS_VECTOR_DB_HOST
)





@shared_task(name="create_embedding_index", max_retries=2, soft_time_limit=600)
def on_create_embedding_index_task(object_pk):
    instance = Embedding.get_or_none(pk=object_pk)
    if instance:
        if instance.isReadyForIndex and not instance.isIndexed:
            key = f"{settings.VECTOR_DB_PREFIX}:{str(instance.id)}"
            try:
                content_embedding = np.array(instance.generated_embedding.get("data",{})[0].get("embedding"), dtype=np.float32).tobytes()                                
                redis_client.hset(key,mapping={"content_vector":content_embedding})            
            except Exception as e:
                instance.hasErrors = True
                instance.lastLog=e.__repr__()
                print("Nao foi possivel indexar")
                logger.error(e.__repr__())
            else:    
                instance.isIndexed=True
                instance.inProgress=False
            
            instance.save()

            print(f"Criado indice para {instance.document_page}")

    #     openai.api_key = instance.document.organization.chatgpt_api_token
    #     instance.num_tokens = len(token_encoding.encode(instance.embedding_raw_content))        
    #     instance.generated_embedding = openai.Embedding.create(input=instance.embedding_raw_content, engine='text-embedding-ada-002')        
    #     instance.save()


@shared_task(name="create_embedding", max_retries=2, soft_time_limit=600)
def on_create_embedding_task(object_pk):
    token_encoding = tiktoken.get_encoding("cl100k_base")
    instance = Embedding.get_or_none(pk=object_pk)
    if instance:
        print(f"Criado incorporacao para {instance}")
        isReadyForIndex = False 
        generated_embedding = {}

        try:
            openai.api_key = instance.document.organization.chatgpt_api_token
            instance.num_tokens = len(token_encoding.encode(instance.embedding_raw_content))  
            generated_embedding = openai.Embedding.create(input=instance.embedding_raw_content, engine='text-embedding-ada-002')        
        except Exception as e:
            instance.hasErrors = True
            generated_embedding = e.__repr__()
            logger.error(e.__repr__())
        else:
            isReadyForIndex=True

        instance.generated_embedding = generated_embedding
        instance.isReadyForIndex=isReadyForIndex
        instance.save()


@shared_task(name="create_embeddings", max_retries=2, soft_time_limit=600)
def on_create_embeddings_task():
    # Run every minute
    # Get the last 100 documents
    objects = Embedding.objects.filter(isIndexed=False,inProgress=False)[0:100]
    for object in objects:
        object.inProgress=True
        object.save()
        app.send_task("create_embedding",[object.id])




@shared_task(name="documents_collection_id_only_embedding", max_retries=2, soft_time_limit=45)
def on_documents_collection_id_only_embedding_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = Embedding.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = EmbeddingIdOnlySerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"documents_collection_id_only_embedding", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")
        
        
@shared_task(name="documents_collection_embedding", max_retries=2, soft_time_limit=45)
def on_documents_collection_id_only_embedding_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = Embedding.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = EmbeddingSerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"documents_collection_embedding", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")



@shared_task(name="stream_live_update_embedding", max_retries=2, soft_time_limit=45)
def on_stream_live_update_embedding_task(object_pk):
    instance = Embedding.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = EmbeddingSerializer(instance)
            async_to_sync(channel_layer.group_send)(
                f"Embedding_{object_pk}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())  