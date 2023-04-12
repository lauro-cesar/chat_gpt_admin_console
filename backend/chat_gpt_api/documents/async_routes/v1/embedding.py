
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path
from documents.consumers import EmbeddingConsumer, EmbeddingCollectionConsumer, EmbeddingCollectionIdOnlyConsumer

async_urlpatterns = [
    path(
        "channels/embedding/collection/",
        EmbeddingCollectionConsumer.as_asgi(),
    ),
    path(
        "channels/embedding/collection-id-only/",
        EmbeddingCollectionIdOnlyConsumer.as_asgi(),
    ),    
    path("channels/embedding/record/view/<object_pk>/", EmbeddingConsumer.as_asgi(), ),
]