
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from project.authentication import APITokenAuthentication
from django.views.generic import View
from django.http import JsonResponse
from django.middleware import csrf
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import json
import re
from django.urls import reverse_lazy
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from project.views import BaseTemplateView
from chats.serializers import QuestionSerializer, QuestionIdOnlySerializer, SerialQuestionSerializer
from chats.models import Question
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView
from project.viewsets import BaseViewSetModel

class QuestionDeleteView(CustomBaseDeleteView):
    template_name = "question/web_templates/v1/question_delete.html"
    model = Question
    success_url = reverse_lazy('question-list')

class QuestionCreateView(CustomBaseCreateView):
    template_name = "question/web_templates/v1/question_create.html"
    model = Question
    fields = Question.CREATE_FIELDS
    success_url = reverse_lazy('question-list')
 

class QuestionUpdateView(CustomBaseUpdateView):
    template_name = "question/web_templates/v1/question_update.html"
    model = Question
    fields = Question.CREATE_FIELDS
 

class QuestionDetailView(CustomBaseDetailView):
    template_name = "question/web_templates/v1/question_detail.html"
    model = Question
 

class QuestionListView(CustomBaseListView):
    template_name = "question/web_templates/v1/question_list.html"
    model = Question
    paginate_by = 15
    allow_empty = True
    
class QuestionTemplateView(BaseTemplateView):
    template_name = "question/web_templates/v1/question_base.html"


class QuestionViewSet(BaseViewSetModel):
   serializer_class = QuestionSerializer

class SerialQuestionViewSet(BaseViewSetModel):
   serializer_class = SerialQuestionSerializer

class QuestionIdOnlyViewSet(BaseViewSetModel):
   serializer_class = QuestionIdOnlySerializer
   