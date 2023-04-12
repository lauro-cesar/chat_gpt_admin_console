
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
from documents.serializers import EmbeddingSerializer, EmbeddingIdOnlySerializer, SerialEmbeddingSerializer
from documents.models import Embedding
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView
from project.viewsets import BaseViewSetModel

class EmbeddingDeleteView(CustomBaseDeleteView):
    template_name = "embedding/web_templates/v1/embedding_delete.html"
    model = Embedding
    success_url = reverse_lazy('embedding-list')

class EmbeddingCreateView(CustomBaseCreateView):
    template_name = "embedding/web_templates/v1/embedding_create.html"
    model = Embedding
    fields = Embedding.CREATE_FIELDS
    success_url = reverse_lazy('embedding-list')
 

class EmbeddingUpdateView(CustomBaseUpdateView):
    template_name = "embedding/web_templates/v1/embedding_update.html"
    model = Embedding
    fields = Embedding.CREATE_FIELDS
 

class EmbeddingDetailView(CustomBaseDetailView):
    template_name = "embedding/web_templates/v1/embedding_detail.html"
    model = Embedding
 

class EmbeddingListView(CustomBaseListView):
    template_name = "embedding/web_templates/v1/embedding_list.html"
    model = Embedding
    paginate_by = 15
    allow_empty = True
    
class EmbeddingTemplateView(BaseTemplateView):
    template_name = "embedding/web_templates/v1/embedding_base.html"


class EmbeddingViewSet(BaseViewSetModel):
   serializer_class = EmbeddingSerializer

class SerialEmbeddingViewSet(BaseViewSetModel):
   serializer_class = SerialEmbeddingSerializer

class EmbeddingIdOnlyViewSet(BaseViewSetModel):
   serializer_class = EmbeddingIdOnlySerializer
   