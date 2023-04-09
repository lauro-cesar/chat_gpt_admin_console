
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
from organizations.serializers import OrganizationSerializer, OrganizationIdOnlySerializer, SerialOrganizationSerializer
from organizations.models import Organization
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView
from project.viewsets import BaseViewSetModel

class OrganizationDeleteView(CustomBaseDeleteView):
    template_name = "organization/web_templates/v1/organization_delete.html"
    model = Organization
    success_url = reverse_lazy('organization-list')

class OrganizationCreateView(CustomBaseCreateView):
    template_name = "organization/web_templates/v1/organization_create.html"
    model = Organization
    fields = Organization.CREATE_FIELDS
    success_url = reverse_lazy('organization-list')
 

class OrganizationUpdateView(CustomBaseUpdateView):
    template_name = "organization/web_templates/v1/organization_update.html"
    model = Organization
    fields = Organization.CREATE_FIELDS
 

class OrganizationDetailView(CustomBaseDetailView):
    template_name = "organization/web_templates/v1/organization_detail.html"
    model = Organization
 

class OrganizationListView(CustomBaseListView):
    template_name = "organization/web_templates/v1/organization_list.html"
    model = Organization
    paginate_by = 15
    allow_empty = True
    
class OrganizationTemplateView(BaseTemplateView):
    template_name = "organization/web_templates/v1/organization_base.html"


class OrganizationViewSet(BaseViewSetModel):
   serializer_class = OrganizationSerializer

class SerialOrganizationViewSet(BaseViewSetModel):
   serializer_class = SerialOrganizationSerializer

class OrganizationIdOnlyViewSet(BaseViewSetModel):
   serializer_class = OrganizationIdOnlySerializer
   