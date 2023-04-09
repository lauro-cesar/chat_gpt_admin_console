
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from chats.views import QuestionViewSet,SerialQuestionViewSet, QuestionIdOnlyViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r'question', QuestionViewSet,basename="question")
router.register(r'serial-question', SerialQuestionViewSet,basename="serial-question")
router.register(r'question-collection-id-only', QuestionIdOnlyViewSet,basename="id-only-question")

urlpatterns = [
	path('', include(router.urls))
]