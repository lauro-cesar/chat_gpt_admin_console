from encodings import utf_8
from urllib import response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.renderers import JSONRenderer
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from django.utils.functional import cached_property
from django.db.models import Count
from datetime import datetime, timedelta
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from accounts.serializers import AccountSerializer
from django.conf import settings


class LoginRequiredForThisView(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"site": self.request.site, "user": self.request.user})
        return context


class CommonBaseView:
    def get_qs_value(self, key_name):
        return self.request.GET.get(f"{key_name}", None)

    def get_bool_qs_value_or_none(self, key_name):
        try:
            key_value = bool(int(self.get_qs_value(key_name)))
        except:
            key_value = None

        if isinstance(key_value, (bool)):
            return key_value
        return None

    def get_int_qs_value_or_default(self, key_name, default_value):
        key_value = self.get_qs_value(key_name)
        if isinstance(key_value, (int)):
            return key_value
        return default_value

    def get_string_qs_value_or_none(self, key_name):
        key_value = self.get_qs_value(key_name)
        if isinstance(key_value, (str)):
            return key_value
        return None

    def get_int_qs_value_or_none(self, key_name):
        key_value = self.get_qs_value(key_name)

        if key_value:
            key_value = int(key_value)

        if isinstance(key_value, (int)):
            return key_value
        return None

    @cached_property
    def next(self):
        return self.get_qs_value("next")

    @cached_property
    def page(self):
        return self.get_int_qs_value_or_default("page", 1)

    @cached_property
    def page_size(self):
        return self.get_int_qs_value_or_default("page_size", 25)

    @cached_property
    def offset(self):
        if int(self.page) > 1:
            return self.page_size * self.page
        return 0


class CustomPublicBaseView(CommonBaseView):
    context_response = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "site": self.request.site,
                "map_credits": '<a target="_sharedway" href="https://www.sharedway.app">SharedWAY&copy;</a> sistemas de alta disponibilidade  Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                "rest_api_address": f"{settings.REST_API_ADDRESS}",
                "socket_api_address": f"{settings.SOCKET_API_ADDRESS}",
                "page": self.page,
                "qs": self.request.GET,
                "page_size": self.page_size,
                "hostname": self.request.headers.get("host"),
            }
        )
        if self.next:
            context.update({"next": self.next})
        return context


class CustomBaseView(CommonBaseView, LoginRequiredForThisView):
    context_response = {}

    @cached_property
    def cache_context(self):
        response = {
            "page": self.page,
            "qs": self.request.GET,
            "page_size": self.page_size,
            "site": self.request.site,
            "hostname": self.request.headers.get("host"),
        }
        return response

    def common_context(self):
        response = self.cache_context
        if self.next:
            response.update({"next": self.next})

        return response


class CustomBaseListView(CustomBaseView, ListView):
    def list_context(self):
        return {}


class CustomBaseDetailView(CustomBaseView, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "rest_api_address": f"{settings.REST_API_ADDRESS}",
                "web_api_address": f"{settings.WEB_API_ADDRESS}",
                "socket_api_address": f"{settings.SOCKET_API_ADDRESS}",
            }
        )
        context.update({"site": self.request.site, "user": self.request.user})
        context.update(self.detail_context())
        contexto = {"contexto": context}

        context.update(contexto)

        return context

    def detail_context(self):
        return {"app_name": "Nome do app"}


class CustomBaseFormView(CustomBaseView, FormView):
    def form_context(self):
        return {}


class CustomBaseCreateView(CustomBaseView, CreateView):
    def create_context(self):
        return {}


class CustomBaseUpdateView(CustomBaseView, UpdateView):
    def update_context(self):
        return {}


class CustomBaseDeleteView(CustomBaseView, DeleteView):
    def delete_context(self):
        return {}


class BaseTemplateView(CustomBaseView, TemplateView):
    def template_context(self):
        return {"site": self.request.site}


class CustomAuthToken(ObtainAuthToken):
    def get(self, request, *args, **kwargs):
        data = {
            "username": request.headers.get("username"),
            "password": request.headers.get("password"),
        }
        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_data = AccountSerializer(user)
        return Response(user_data.data)


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_data = AccountSerializer(user)
        return Response(user_data.data)
