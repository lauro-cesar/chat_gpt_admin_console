
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path
from chats.consumers import ChatSessionConsumer, ChatSessionCollectionConsumer, ChatSessionCollectionIdOnlyConsumer

async_urlpatterns = [
    path(
        "channels/chatsession/collection/",
        ChatSessionCollectionConsumer.as_asgi(),
    ),
    path(
        "channels/chatsession/collection-id-only/",
        ChatSessionCollectionIdOnlyConsumer.as_asgi(),
    ),    
    path("channels/chatsession/record/view/<object_pk>/", ChatSessionConsumer.as_asgi(), ),
]