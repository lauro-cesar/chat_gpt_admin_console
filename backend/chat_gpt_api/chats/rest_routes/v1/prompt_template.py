
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from chats.views import PromptTemplateViewSet,SerialPromptTemplateViewSet, PromptTemplateIdOnlyViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r'prompttemplate', PromptTemplateViewSet,basename="prompttemplate")
# router.register(r'serial-prompttemplate', SerialPromptTemplateViewSet,basename="serial-prompttemplate")
# router.register(r'prompttemplate-collection-id-only', PromptTemplateIdOnlyViewSet,basename="id-only-prompttemplate")

urlpatterns = [
	path('', include(router.urls))
]