
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path
from documents.consumers import DocumentConsumer, DocumentCollectionConsumer, DocumentCollectionIdOnlyConsumer

async_urlpatterns = [
    path(
        "channels/document/collection/",
        DocumentCollectionConsumer.as_asgi(),
    ),
    path(
        "channels/document/collection-id-only/",
        DocumentCollectionIdOnlyConsumer.as_asgi(),
    ),    
    path("channels/document/record/view/<object_pk>/", DocumentConsumer.as_asgi(), ),
]