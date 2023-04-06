from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from project.authentication import APITokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework import generics


class BaseViewSetModel(viewsets.ModelViewSet):
    ENABLE_READ_ONLY = False
    permission_classes = [IsAuthenticated]
    authentication_classes = [APITokenAuthentication, SessionAuthentication]
    parser_classes = [JSONParser]

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(never_cache)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Lets check if this user has permission to create this model:
        return super().create(request, *args, **kwargs)
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_context(self):
        return {
            "request_by": self.request.user,
            "criado_por": self.request.user,
            "modificado_por": self.request.user,
            "request": self.request,  # request object is passed here
            "format": self.format_kwarg,
            "view": self,
        }

    # def get_queryset(self):
    #     qs = self.serializer_class.Meta.model._default_manager.get_queryset()
    #     user = self.request.user
    #     if True not in [user.is_superuser, user.is_operator]:
    #         qs = qs.filter(criado_por=user)
    #     return qs

    def get_queryset(self):
        qs = self.serializer_class.Meta.model._default_manager.get_queryset()

        if not self.ENABLE_READ_ONLY:
            user = self.request.user
            checklist = []
            if hasattr(user, "is_superuser"):
                checklist.append(user.is_superuser)
            if hasattr(user, "is_operator"):
                checklist.append(user.is_operator)
            if True not in checklist:
                qs = qs.filter(criado_por=user)

        return qs
