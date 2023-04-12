
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from documents.views import EmbeddingViewSet,SerialEmbeddingViewSet, EmbeddingIdOnlyViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r'embedding', EmbeddingViewSet,basename="embedding")
router.register(r'serial-embedding', SerialEmbeddingViewSet,basename="serial-embedding")
router.register(r'embedding-collection-id-only', EmbeddingIdOnlyViewSet,basename="id-only-embedding")

urlpatterns = [
	path('', include(router.urls))
]