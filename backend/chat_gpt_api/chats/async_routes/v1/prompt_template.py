
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path
from chats.consumers import PromptTemplateConsumer, PromptTemplateCollectionConsumer, PromptTemplateCollectionIdOnlyConsumer

async_urlpatterns = [
    path(
        "channels/prompttemplate/collection/",
        PromptTemplateCollectionConsumer.as_asgi(),
    ),
    path(
        "channels/prompttemplate/collection-id-only/",
        PromptTemplateCollectionIdOnlyConsumer.as_asgi(),
    ),    
    path("channels/prompttemplate/record/view/<object_pk>/", PromptTemplateConsumer.as_asgi(), ),
]