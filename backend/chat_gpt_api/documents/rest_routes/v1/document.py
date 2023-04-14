
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from documents.views import DocumentViewSet,SerialDocumentViewSet, DocumentIdOnlyViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r'document', DocumentViewSet,basename="document")
# router.register(r'serial-document', SerialDocumentViewSet,basename="serial-document")
# router.register(r'document-collection-id-only', DocumentIdOnlyViewSet,basename="id-only-document")

urlpatterns = [
	path('', include(router.urls))
]