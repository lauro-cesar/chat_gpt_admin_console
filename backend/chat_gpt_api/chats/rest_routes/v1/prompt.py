
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from chats.views import PromptViewSet,SerialPromptViewSet, PromptIdOnlyViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r'prompt', PromptViewSet,basename="prompt")
# router.register(r'serial-prompt', SerialPromptViewSet,basename="serial-prompt")
# router.register(r'prompt-collection-id-only', PromptIdOnlyViewSet,basename="id-only-prompt")

urlpatterns = [
	path('', include(router.urls))
]