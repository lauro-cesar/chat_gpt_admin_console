
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
from chats.serializers import ChatSessionSerializer, ChatSessionIdOnlySerializer, SerialChatSessionSerializer
from chats.models import ChatSession
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView
from project.viewsets import BaseViewSetModel

class ChatSessionDeleteView(CustomBaseDeleteView):
    template_name = "chatsession/web_templates/v1/chatsession_delete.html"
    model = ChatSession
    success_url = reverse_lazy('chatsession-list')

class ChatSessionCreateView(CustomBaseCreateView):
    template_name = "chatsession/web_templates/v1/chatsession_create.html"
    model = ChatSession
    fields = ChatSession.CREATE_FIELDS
    success_url = reverse_lazy('chatsession-list')
 

class ChatSessionUpdateView(CustomBaseUpdateView):
    template_name = "chatsession/web_templates/v1/chatsession_update.html"
    model = ChatSession
    fields = ChatSession.CREATE_FIELDS
 

class ChatSessionDetailView(CustomBaseDetailView):
    template_name = "chatsession/web_templates/v1/chatsession_detail.html"
    model = ChatSession
 

class ChatSessionListView(CustomBaseListView):
    template_name = "chatsession/web_templates/v1/chatsession_list.html"
    model = ChatSession
    paginate_by = 15
    allow_empty = True
    
class ChatSessionTemplateView(BaseTemplateView):
    template_name = "chatsession/web_templates/v1/chatsession_base.html"


class ChatSessionViewSet(BaseViewSetModel):
   serializer_class = ChatSessionSerializer

class SerialChatSessionViewSet(BaseViewSetModel):
   serializer_class = SerialChatSessionSerializer

class ChatSessionIdOnlyViewSet(BaseViewSetModel):
   serializer_class = ChatSessionIdOnlySerializer
   