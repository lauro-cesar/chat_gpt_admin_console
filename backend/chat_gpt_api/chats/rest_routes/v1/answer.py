
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from chats.views import AnswerViewSet,SerialAnswerViewSet, AnswerIdOnlyViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r'answer', AnswerViewSet,basename="answer")
router.register(r'serial-answer', SerialAnswerViewSet,basename="serial-answer")
router.register(r'answer-collection-id-only', AnswerIdOnlyViewSet,basename="id-only-answer")

urlpatterns = [
	path('', include(router.urls))
]