
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
from organizations.serializers import KnowledgeBaseSerializer, KnowledgeBaseIdOnlySerializer, SerialKnowledgeBaseSerializer
from organizations.models import KnowledgeBase
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView
from project.viewsets import BaseViewSetModel

class KnowledgeBaseDeleteView(CustomBaseDeleteView):
    template_name = "knowledgebase/web_templates/v1/knowledgebase_delete.html"
    model = KnowledgeBase
    success_url = reverse_lazy('knowledgebase-list')

class KnowledgeBaseCreateView(CustomBaseCreateView):
    template_name = "knowledgebase/web_templates/v1/knowledgebase_create.html"
    model = KnowledgeBase
    fields = KnowledgeBase.CREATE_FIELDS
    success_url = reverse_lazy('knowledgebase-list')
 

class KnowledgeBaseUpdateView(CustomBaseUpdateView):
    template_name = "knowledgebase/web_templates/v1/knowledgebase_update.html"
    model = KnowledgeBase
    fields = KnowledgeBase.CREATE_FIELDS
 

class KnowledgeBaseDetailView(CustomBaseDetailView):
    template_name = "knowledgebase/web_templates/v1/knowledgebase_detail.html"
    model = KnowledgeBase
 

class KnowledgeBaseListView(CustomBaseListView):
    template_name = "knowledgebase/web_templates/v1/knowledgebase_list.html"
    model = KnowledgeBase
    paginate_by = 15
    allow_empty = True
    
class KnowledgeBaseTemplateView(BaseTemplateView):
    template_name = "knowledgebase/web_templates/v1/knowledgebase_base.html"


class KnowledgeBaseViewSet(BaseViewSetModel):
   serializer_class = KnowledgeBaseSerializer

class SerialKnowledgeBaseViewSet(BaseViewSetModel):
   serializer_class = SerialKnowledgeBaseSerializer

class KnowledgeBaseIdOnlyViewSet(BaseViewSetModel):
   serializer_class = KnowledgeBaseIdOnlySerializer
   