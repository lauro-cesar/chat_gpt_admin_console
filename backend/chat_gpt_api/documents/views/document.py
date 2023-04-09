
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
from documents.serializers import DocumentSerializer, DocumentIdOnlySerializer, SerialDocumentSerializer
from documents.models import Document
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView
from project.viewsets import BaseViewSetModel

class DocumentDeleteView(CustomBaseDeleteView):
    template_name = "document/web_templates/v1/document_delete.html"
    model = Document
    success_url = reverse_lazy('document-list')

class DocumentCreateView(CustomBaseCreateView):
    template_name = "document/web_templates/v1/document_create.html"
    model = Document
    fields = Document.CREATE_FIELDS
    success_url = reverse_lazy('document-list')
 

class DocumentUpdateView(CustomBaseUpdateView):
    template_name = "document/web_templates/v1/document_update.html"
    model = Document
    fields = Document.CREATE_FIELDS
 

class DocumentDetailView(CustomBaseDetailView):
    template_name = "document/web_templates/v1/document_detail.html"
    model = Document
 

class DocumentListView(CustomBaseListView):
    template_name = "document/web_templates/v1/document_list.html"
    model = Document
    paginate_by = 15
    allow_empty = True
    
class DocumentTemplateView(BaseTemplateView):
    template_name = "document/web_templates/v1/document_base.html"


class DocumentViewSet(BaseViewSetModel):
   serializer_class = DocumentSerializer

class SerialDocumentViewSet(BaseViewSetModel):
   serializer_class = SerialDocumentSerializer

class DocumentIdOnlyViewSet(BaseViewSetModel):
   serializer_class = DocumentIdOnlySerializer
   