
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from organizations.views import KnowledgeBaseViewSet,SerialKnowledgeBaseViewSet, KnowledgeBaseIdOnlyViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r'knowledgebase', KnowledgeBaseViewSet,basename="knowledgebase")
# router.register(r'serial-knowledgebase', SerialKnowledgeBaseViewSet,basename="serial-knowledgebase")
# router.register(r'knowledgebase-collection-id-only', KnowledgeBaseIdOnlyViewSet,basename="id-only-knowledgebase")

urlpatterns = [
	path('', include(router.urls))
]