from django.urls import path
from accounts.consumers import (
    AccountTypeConsumer,
    AccountTypeCollectionConsumer,
    AccountTypeCollectionIdOnlyConsumer,
)

async_urlpatterns = [
    path(
        "channels/accounttype/collection/",
        AccountTypeCollectionConsumer.as_asgi(),
    ),
    path(
        "channels/accounttype/collection-id-only/",
        AccountTypeCollectionIdOnlyConsumer.as_asgi(),
    ),
    path(
        "channels/accounttype/record/view/<object_pk>/",
        AccountTypeConsumer.as_asgi(),
    ),
]
