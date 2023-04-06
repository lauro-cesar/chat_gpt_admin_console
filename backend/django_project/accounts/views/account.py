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
from accounts.serializers import AccountSerializer
from accounts.forms import UserCreateForm
from project.views import (
    CustomBaseListView,
    CustomBaseDetailView,
    CustomBaseUpdateView,
    CustomBaseCreateView,
    CustomBaseDeleteView,
    CommonBaseView,
)
from project.viewsets import BaseViewSetModel
from django.views.generic.edit import CreateView
from django.contrib.auth import (
    authenticate,
    get_user_model,
    password_validation,
)

Account = get_user_model()


class AccountDeleteView(CustomBaseDeleteView):
    template_name = "account/web_templates/v1/account_delete.html"
    model = Account
    success_url = reverse_lazy("account-list")


class AccountCreateView(CommonBaseView, CreateView):
    def get(self, request):
        return JsonResponse({"csrftoken": "%s" % csrf.get_token(request)}, status=200)

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            user_data = AccountSerializer(user)
            return JsonResponse(
                user_data.data,
                status=201,
            )
        return JsonResponse({"message": f"Error: {form.errors}"}, status=400)

    template_name = "account/web_templates/v1/account_create.html"
    model = Account
    form_class = UserCreateForm
    success_url = reverse_lazy("account-list")


class AccountUpdateView(CustomBaseUpdateView):
    template_name = "account/web_templates/v1/account_update.html"
    model = Account
    fields = Account.CREATE_FIELDS


class AccountDetailView(CustomBaseDetailView):
    template_name = "account/web_templates/v1/account_detail.html"
    model = Account


class AccountListView(CustomBaseListView):
    template_name = "account/web_templates/v1/account_list.html"
    model = Account
    paginate_by = 15
    allow_empty = True


class AccountTemplateView(BaseTemplateView):
    template_name = "account/web_templates/v1/account_base.html"


class AccountViewSet(BaseViewSetModel):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [APITokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return get_user_model().objects.filter(pk=user.id)
