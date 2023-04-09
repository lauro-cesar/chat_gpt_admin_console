
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
from chats.serializers import PromptSerializer, PromptIdOnlySerializer, SerialPromptSerializer
from chats.models import Prompt
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView
from project.viewsets import BaseViewSetModel

class PromptDeleteView(CustomBaseDeleteView):
    template_name = "prompt/web_templates/v1/prompt_delete.html"
    model = Prompt
    success_url = reverse_lazy('prompt-list')

class PromptCreateView(CustomBaseCreateView):
    template_name = "prompt/web_templates/v1/prompt_create.html"
    model = Prompt
    fields = Prompt.CREATE_FIELDS
    success_url = reverse_lazy('prompt-list')
 

class PromptUpdateView(CustomBaseUpdateView):
    template_name = "prompt/web_templates/v1/prompt_update.html"
    model = Prompt
    fields = Prompt.CREATE_FIELDS
 

class PromptDetailView(CustomBaseDetailView):
    template_name = "prompt/web_templates/v1/prompt_detail.html"
    model = Prompt
 

class PromptListView(CustomBaseListView):
    template_name = "prompt/web_templates/v1/prompt_list.html"
    model = Prompt
    paginate_by = 15
    allow_empty = True
    
class PromptTemplateView(BaseTemplateView):
    template_name = "prompt/web_templates/v1/prompt_base.html"


class PromptViewSet(BaseViewSetModel):
   serializer_class = PromptSerializer

class SerialPromptViewSet(BaseViewSetModel):
   serializer_class = SerialPromptSerializer

class PromptIdOnlyViewSet(BaseViewSetModel):
   serializer_class = PromptIdOnlySerializer
   