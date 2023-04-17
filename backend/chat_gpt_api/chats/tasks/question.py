
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
from chats.models import Question, Answer
from chats.serializers import QuestionSerializer, QuestionIdOnlySerializer

import tiktoken
import openai
import redis
import numpy as np

# from openai.embeddings_utils import (
  
#     distances_from_embeddings,
#     tsne_components_from_embeddings,
  
#     indices_of_nearest_neighbors_from_distances,
# )


from redis.commands.search.query import Query

redis_client = redis.Redis(password=settings.REDIS_VECTOR_DB_PASSWORD,port=settings.REDIS_VECTOR_DB_PORT,host=settings.REDIS_VECTOR_DB_HOST)


@shared_task(name="retrieve_answer", max_retries=2, soft_time_limit=600)
def on_retrieve_answer_task(question_pk):
    token_encoding = tiktoken.get_encoding("cl100k_base")
    question = Question.get_or_none(pk=question_pk,hasErrors=False)
    if question:
        separator_len = len(token_encoding.encode("\n*"))

        print("Ask question")
        print(question.chat_session.prompt.knowledge_base)
        print(question.chat_session.prompt.knowledge_base.vector_index_name)
        print(question.chat_session.prompt.knowledge_base.vector_prefix)
        print(question.chat_session.prompt.prompt_command)


        # MAX_CONTEXT_SIZE


        

     
        context_entries=[]

    
        try:
            hybrid_fields = "*"
            k= 20
            return_fields= ["vector_score","embedding_raw_content","generated_embedding"]
            vector_field = "generated_embedding"
            base_query = f'{hybrid_fields}=>[KNN {k} @{vector_field} $vector AS vector_score]'
            query = (Query(base_query).return_fields(*return_fields).sort_by("vector_score").paging(0, k).dialect(2))            
            params_dict = {"vector": np.array(question.embedded_query).astype(dtype=np.float32).tobytes()}        
            results = redis_client.ft(question.chat_session.prompt.knowledge_base.vector_index_name).search(query, params_dict)  

          

            for i, result in enumerate(results.docs):
                score = 1 - float(result.vector_score)

                if(score >=settings.COSINE_SIM_THRESHOLD):
                    prompt_context = "\n".join(context_entries)

                    total_tokens = token_encoding.encode(prompt_context).__len__()
                    if total_tokens < settings.MAX_CONTEXT_SIZE:                       
                        context_entries.append(result.embedding_raw_content)

                    # print(settings.COSINE_SIM_THRESHOLD)
                    # print(result.vector_score)

                    # tokens = token_encoding.encode(result.embedding_raw_content)
                    # print(len(tokens))
                    # print(separator_len)
                

                    # print(len())

                    




              


           
                

    
                
        

        except Exception as e:
            print(e.__repr__())
        
        else:

            header = f"""{question.chat_session.prompt.prompt_command}\n\nContext:{prompt_context}\n\nQuestion:{question.question_content}"""
            openai.api_key = question.chat_session.prompt.knowledge_base.organization.chatgpt_api_token
            query = f""" """
            MODEL = "text-davinci-003"

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=question.chat_session.prompt.prompt_temperature,
                max_tokens=question.chat_session.prompt.prompt_max_tokens,
                top_p=1,
                frequency_penalty=question.chat_session.prompt.prompt_frequency_penalty,
                presence_penalty=question.chat_session.prompt.prompt_presence_penalty,                
                messages=[
                    {"role": "system", "content": f"{question.chat_session.prompt.prompt_command}"},
                    {"role": "user", "content": f"{question.question_content}"},
                ]               
            )["choices"][0].get("message",{}).get("content","Nada Encontrado")



            # resposta = openai.Completion.create(
            #     prompt=header,
            #     temperature=question.chat_session.prompt.prompt_temperature,
            #     max_tokens=question.chat_session.prompt.prompt_max_tokens,
            #     top_p=1,
            #     frequency_penalty=question.chat_session.prompt.prompt_frequency_penalty,
            #     presence_penalty=question.chat_session.prompt.prompt_presence_penalty,
            #     model= MODEL

            # )["choices"][0]["text"].strip(" \n")



            answer = Answer.objects.create(**{
                "answer_content":response
            })
            answer.save()
            question.answer = answer
            question.isReady = True
            question.save()
            print(response)



            # resposta = openai.Completion.create(
            #     prompt=header,
            #     temperature=0,
            #     max_tokens=settings.MAX_CONTEXT_SIZE,
            #     top_p=1,
            #     frequency_penalty=0,
            #     presence_penalty=0,
            #     model= question.chat_session.prompt.prompt_model
            # )["choices"][0]["text"].strip(" \n")



    # 
    # question.save()
    # 
    # Send task to retrieve answer


@shared_task(name="prepare_question", max_retries=2, soft_time_limit=600)
def on_prepare_question_task(question_pk):
    token_encoding = tiktoken.get_encoding("cl100k_base")
    question = Question.get_or_none(pk=question_pk,isReadyToAsk=False,hasErrors=False)
    if question:
        print(question.chat_session.prompt.knowledge_base.organization.chatgpt_api_token)
        
        try:
            openai.api_key = question.chat_session.prompt.knowledge_base.organization.chatgpt_api_token
            question.num_tokens = len(token_encoding.encode(question.question_content))        
            question.generated_embedding = openai.Embedding.create(input=question.question_content, engine='text-embedding-ada-002')   
        except Exception as e:                
            question.lastLog=e.__repr__()
            question.hasErrors=True
            question.save()            
            logger.error(e.__repr__())
        else:
            question.hasErrors=False
            question.isReadyToAsk = True
            question.save()
            app.send_task("retrieve_answer",[question_pk])

            
        logger.info(f"Buscando resposta para pergunta {question} usando o prompt: {question.chat_session.prompt}")





@shared_task(name="chats_collection_id_only_question", max_retries=2, soft_time_limit=45)
def on_chats_collection_id_only_question_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = Question.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = QuestionIdOnlySerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"chats_collection_id_only_question", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")
        
        
@shared_task(name="chats_collection_question", max_retries=2, soft_time_limit=45)
def on_chats_collection_id_only_question_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = Question.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = QuestionSerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"chats_collection_question", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")



@shared_task(name="stream_live_update_question", max_retries=2, soft_time_limit=45)
def on_stream_live_update_question_task(object_pk):
    instance = Question.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = QuestionSerializer(instance)
            async_to_sync(channel_layer.group_send)(
                f"Question_{object_pk}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())  