
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
from chats.serializers import PromptTemplateSerializer, PromptTemplateIdOnlySerializer, SerialPromptTemplateSerializer
from chats.models import PromptTemplate
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView
from project.viewsets import BaseViewSetModel

class PromptTemplateDeleteView(CustomBaseDeleteView):
    template_name = "prompttemplate/web_templates/v1/prompttemplate_delete.html"
    model = PromptTemplate
    success_url = reverse_lazy('prompttemplate-list')

class PromptTemplateCreateView(CustomBaseCreateView):
    template_name = "prompttemplate/web_templates/v1/prompttemplate_create.html"
    model = PromptTemplate
    fields = PromptTemplate.CREATE_FIELDS
    success_url = reverse_lazy('prompttemplate-list')
 

class PromptTemplateUpdateView(CustomBaseUpdateView):
    template_name = "prompttemplate/web_templates/v1/prompttemplate_update.html"
    model = PromptTemplate
    fields = PromptTemplate.CREATE_FIELDS
 

class PromptTemplateDetailView(CustomBaseDetailView):
    template_name = "prompttemplate/web_templates/v1/prompttemplate_detail.html"
    model = PromptTemplate
 

class PromptTemplateListView(CustomBaseListView):
    template_name = "prompttemplate/web_templates/v1/prompttemplate_list.html"
    model = PromptTemplate
    paginate_by = 15
    allow_empty = True
    
class PromptTemplateTemplateView(BaseTemplateView):
    template_name = "prompttemplate/web_templates/v1/prompttemplate_base.html"


class PromptTemplateViewSet(BaseViewSetModel):
   serializer_class = PromptTemplateSerializer

class SerialPromptTemplateViewSet(BaseViewSetModel):
   serializer_class = SerialPromptTemplateSerializer

class PromptTemplateIdOnlyViewSet(BaseViewSetModel):
   serializer_class = PromptTemplateIdOnlySerializer
   