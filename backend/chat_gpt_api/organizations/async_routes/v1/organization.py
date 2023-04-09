
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path
from organizations.consumers import OrganizationConsumer, OrganizationCollectionConsumer, OrganizationCollectionIdOnlyConsumer

async_urlpatterns = [
    path(
        "channels/organization/collection/",
        OrganizationCollectionConsumer.as_asgi(),
    ),
    path(
        "channels/organization/collection-id-only/",
        OrganizationCollectionIdOnlyConsumer.as_asgi(),
    ),    
    path("channels/organization/record/view/<object_pk>/", OrganizationConsumer.as_asgi(), ),
]