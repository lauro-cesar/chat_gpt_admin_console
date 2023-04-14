
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from chats.views import ChatSessionViewSet,SerialChatSessionViewSet, ChatSessionIdOnlyViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r'chatsession', ChatSessionViewSet,basename="chatsession")
# router.register(r'serial-chatsession', SerialChatSessionViewSet,basename="serial-chatsession")
# router.register(r'chatsession-collection-id-only', ChatSessionIdOnlyViewSet,basename="id-only-chatsession")

urlpatterns = [
	path('', include(router.urls))
]