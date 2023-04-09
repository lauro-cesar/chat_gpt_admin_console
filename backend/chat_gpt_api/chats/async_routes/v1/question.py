
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path
from chats.consumers import QuestionConsumer, QuestionCollectionConsumer, QuestionCollectionIdOnlyConsumer

async_urlpatterns = [
    path(
        "channels/question/collection/",
        QuestionCollectionConsumer.as_asgi(),
    ),
    path(
        "channels/question/collection-id-only/",
        QuestionCollectionIdOnlyConsumer.as_asgi(),
    ),    
    path("channels/question/record/view/<object_pk>/", QuestionConsumer.as_asgi(), ),
]