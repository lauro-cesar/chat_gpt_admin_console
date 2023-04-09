
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
from chats.serializers import AnswerSerializer, AnswerIdOnlySerializer, SerialAnswerSerializer
from chats.models import Answer
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView
from project.viewsets import BaseViewSetModel

class AnswerDeleteView(CustomBaseDeleteView):
    template_name = "answer/web_templates/v1/answer_delete.html"
    model = Answer
    success_url = reverse_lazy('answer-list')

class AnswerCreateView(CustomBaseCreateView):
    template_name = "answer/web_templates/v1/answer_create.html"
    model = Answer
    fields = Answer.CREATE_FIELDS
    success_url = reverse_lazy('answer-list')
 

class AnswerUpdateView(CustomBaseUpdateView):
    template_name = "answer/web_templates/v1/answer_update.html"
    model = Answer
    fields = Answer.CREATE_FIELDS
 

class AnswerDetailView(CustomBaseDetailView):
    template_name = "answer/web_templates/v1/answer_detail.html"
    model = Answer
 

class AnswerListView(CustomBaseListView):
    template_name = "answer/web_templates/v1/answer_list.html"
    model = Answer
    paginate_by = 15
    allow_empty = True
    
class AnswerTemplateView(BaseTemplateView):
    template_name = "answer/web_templates/v1/answer_base.html"


class AnswerViewSet(BaseViewSetModel):
   serializer_class = AnswerSerializer

class SerialAnswerViewSet(BaseViewSetModel):
   serializer_class = SerialAnswerSerializer

class AnswerIdOnlyViewSet(BaseViewSetModel):
   serializer_class = AnswerIdOnlySerializer
   