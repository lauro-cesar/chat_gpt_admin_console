
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path
from chats.consumers import PromptConsumer, PromptCollectionConsumer, PromptCollectionIdOnlyConsumer

async_urlpatterns = [
    path(
        "channels/prompt/collection/",
        PromptCollectionConsumer.as_asgi(),
    ),
    path(
        "channels/prompt/collection-id-only/",
        PromptCollectionIdOnlyConsumer.as_asgi(),
    ),    
    path("channels/prompt/record/view/<object_pk>/", PromptConsumer.as_asgi(), ),
]