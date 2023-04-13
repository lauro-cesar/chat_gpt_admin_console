
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
from chats.models import Prompt, Question, Answer
from chats.serializers import PromptSerializer, PromptIdOnlySerializer

import tiktoken
import openai
import redis
import numpy as np

from redis.commands.search.query import Query

redis_client = redis.Redis(password=settings.REDIS_VECTOR_DB_PASSWORD,port=settings.REDIS_VECTOR_DB_PORT,host=settings.REDIS_VECTOR_DB_HOST)



@shared_task(name="retrieve_answer", max_retries=2, soft_time_limit=600)
def on_retrieve_answer_task(question_pk):
    print(f"Retrieve answer for: {question_pk}")


@shared_task(name="prepare_question", max_retries=2, soft_time_limit=600)
def on_prepare_question_task(question_pk):
    question = Question.get_or_none(pk=question_pk,isReadyToAsk=False,hasErrors=False)
    
    if question:
        print("Preparando a pergunta")
        token_encoding = tiktoken.get_encoding("cl100k_base")
        try:
            openai.api_key = question.prompt.organization.chatgpt_api_token
            question.num_tokens = len(token_encoding.encode(question.question_content))        
            question.generated_embedding = openai.Embedding.create(input=question.question_content, engine='text-embedding-ada-002')   
        except Exception as e:                
            question.lastLog=e.__repr__()
            question.hasErrors=True
            question.save()            
            logger.error(e.__repr__())
        else:
            print(redis_client.ft(settings.VECTOR_DB_HNSW_INDEX_NAME).info())

            try:
                hybrid_fields = "*"
                k= 10
                return_fields= ["vector_score"]
                vector_field = "content_vector"
                base_query = f'{hybrid_fields}=>[KNN {k} @{vector_field} $vector AS vector_score]'
                query = (Query(base_query).return_fields(*return_fields).sort_by("vector_score").paging(0, k).dialect(2))            
                params_dict = {"vector": np.array(question.embedded_query).astype(dtype=np.float32).tobytes()}
                results = redis_client.ft(settings.VECTOR_DB_HNSW_INDEX_NAME).search(query, params_dict)
               
                print(results)


                for i, article in enumerate(results.docs):
                    score = 1 - float(article.vector_score)
                    print(f"{i}. {article.title} (Score: {round(score ,3) })")
            
            except Exception as e:
                print(e.__repr__())

            question.hasErrors=False
            question.isReadyToAsk = True
            question.save()
            app.send_task("retrieve_answer",[question_pk])
            # Send task to retrieve answer

        logger.info(f"Buscando resposta para pergunta {question} usando o prompt: {question.prompt}")





@shared_task(name="chats_collection_id_only_prompt", max_retries=2, soft_time_limit=45)
def on_chats_collection_id_only_prompt_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = Prompt.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = PromptIdOnlySerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"chats_collection_id_only_prompt", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")
        
        
@shared_task(name="chats_collection_prompt", max_retries=2, soft_time_limit=45)
def on_chats_collection_id_only_prompt_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = Prompt.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = PromptSerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"chats_collection_prompt", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")



@shared_task(name="stream_live_update_prompt", max_retries=2, soft_time_limit=45)
def on_stream_live_update_prompt_task(object_pk):
    instance = Prompt.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = PromptSerializer(instance)
            async_to_sync(channel_layer.group_send)(
                f"Prompt_{object_pk}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())  