
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path
from chats.consumers import AnswerConsumer, AnswerCollectionConsumer, AnswerCollectionIdOnlyConsumer

async_urlpatterns = [
    path(
        "channels/answer/collection/",
        AnswerCollectionConsumer.as_asgi(),
    ),
    path(
        "channels/answer/collection-id-only/",
        AnswerCollectionIdOnlyConsumer.as_asgi(),
    ),    
    path("channels/answer/record/view/<object_pk>/", AnswerConsumer.as_asgi(), ),
]