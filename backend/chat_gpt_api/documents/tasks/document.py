
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
from documents.models import Document
from documents.serializers import DocumentSerializer, DocumentIdOnlySerializer
from PyPDF2 import PdfReader
import tiktoken
import openai
import redis
import numpy as np


def chunks(text, n, tokenizer):
    tokens = tokenizer.encode(text)
    """Yield successive n-sized chunks from text."""
    i = 0
    while i < len(tokens):
        # Find the nearest end of sentence within a range of 0.5 * n and 1.5 * n tokens
        j = min(i + int(1.5 * n), len(tokens))
        while j > i + int(0.5 * n):
            # Decode the tokens and check for full stop or newline
            chunk = tokenizer.decode(tokens[i:j])
            if chunk.endswith(".") or chunk.endswith("\n"):
                break
            j -= 1
        # If no end of sentence found, use n tokens as the chunk size
        if j == i + int(0.5 * n):
            j = min(i + n, len(tokens))
        yield tokens[i:j]
        i = j



@shared_task(name="consolida_documento_indexado", max_retries=2, soft_time_limit=600)
def on_consolida_documento_indexado_task(object_pk):
    logger.info(f"Consolidando documento: {object_pk}")
    instance = Document.get_or_none(pk=object_pk)
    total_docs = instance.document_embeddings.count()
    total_indexado = instance.document_embeddings.filter(isIndexed=True).count()
    if total_docs == total_indexado:
        instance.isIndexed=True 
        instance.inProgress=False 
        instance.save()

    



@shared_task(name="monitora_indexador", max_retries=2, soft_time_limit=600)
def on_monitora_indexador_task():
    # Verifica o status dos documentos nao indexados
    documentos = Document.objects.filter(isIndexed=False,inProgress=True)[0:100]
    logger.info(f"Consolidando documentos: {documentos.count()}")
    for documento in documentos:
        app.send_task("consolida_documento_indexado",[documento.id])


@shared_task(name="extract_raw_embedding", max_retries=2, soft_time_limit=600)
def on_extract_raw_embedding_task(object_pk):
    instance = Document.get_or_none(pk=object_pk)
    token_encoding = tiktoken.get_encoding("cl100k_base")
    
    try:
        instance.document_embeddings.all().delete()
    except Exception as e:
        logger.error(e.__repr__())

    pdf_obj = PdfReader(instance.document_file.path)
    page =1
    instance.inProgress=True 
    instance.isIndexed=False
    instance.save()

    for p in pdf_obj.pages:
        texto = p.extract_text()
        texto = texto.strip().replace("\n", "; ").replace("  ", " ")
        token_chunks = list(chunks(texto, settings.TEXT_EMBEDDING_CHUNK_SIZE, token_encoding))
        text_chunks = [token_encoding.decode(chunk) for chunk in token_chunks]
        text_chunks_list = [text_chunks[i:i+settings.MAX_TEXTS_TO_EMBED_BATCH_SIZE] for i in range(0, len(text_chunks), settings.MAX_TEXTS_TO_EMBED_BATCH_SIZE)]

        #TODO: Send to another task
        for text_chunk in text_chunks_list:
            instance.document_embeddings.create(**{
                "document_page":page,
                "embedding_raw_content":" ".join(text_chunk)})
        page +=1

    logger.info(f"Extracting Raw embedding for {instance}")


@shared_task(name="documents_collection_id_only_document", max_retries=2, soft_time_limit=45)
def on_documents_collection_id_only_document_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = Document.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = DocumentIdOnlySerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"documents_collection_id_only_document", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")
        
        
@shared_task(name="documents_collection_document", max_retries=2, soft_time_limit=45)
def on_documents_collection_id_only_document_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = Document.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = DocumentSerializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"documents_collection_document", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")



@shared_task(name="stream_live_update_document", max_retries=2, soft_time_limit=45)
def on_stream_live_update_document_task(object_pk):
    instance = Document.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = DocumentSerializer(instance)
            async_to_sync(channel_layer.group_send)(
                f"Document_{object_pk}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())  