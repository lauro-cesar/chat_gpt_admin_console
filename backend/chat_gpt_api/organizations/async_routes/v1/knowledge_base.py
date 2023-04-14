
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path
from organizations.consumers import KnowledgeBaseConsumer, KnowledgeBaseCollectionConsumer, KnowledgeBaseCollectionIdOnlyConsumer

async_urlpatterns = [
    path(
        "channels/knowledgebase/collection/",
        KnowledgeBaseCollectionConsumer.as_asgi(),
    ),
    path(
        "channels/knowledgebase/collection-id-only/",
        KnowledgeBaseCollectionIdOnlyConsumer.as_asgi(),
    ),    
    path("channels/knowledgebase/record/view/<object_pk>/", KnowledgeBaseConsumer.as_asgi(), ),
]