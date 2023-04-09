"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
import logging
logger = logging.getLogger(__name__)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from django.conf import settings
import base64
from django.urls import reverse
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from project.models import BaseModel, StackedModel
from django.db import models
from django.contrib.auth.models import AbstractUser, User, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from datetime import datetime


class Account(AbstractUser, BaseModel):
    SERIALIZABLES = [
        "username",
        "email",
        "first_name",
        "last_name",
        "id",
        "authToken",
    ]
    READ_ONLY_FIELDS = []
    ADMIN_LIST_EDITABLE = []
    ADMIN_LIST_DISPLAY = ["username", "first_name", "last_name","is_operator","is_rootuser"]
    ADMIN_ORDERING = []
    ADMIN_FILTER_HORIZONTAL = ["groups", "user_permissions"]
    ADMIN_LIST_FILTER = []
    ADMIN_SEARCH_FILTER = []
    ADMIN_DISPLAY_LINKS = []
    EXCLUDE_FROM_ADMIN = []
    CREATE_FIELDS = []
    FORM_FIELDS = []
    REST_BASENAME = "account"

    TASKS = {
        "on_create": [],
        "on_save": [],
        "on_delete": [],
    }
    dateCreated = models.DateTimeField(auto_now=True)
    lastModified = models.DateTimeField(auto_now=True)
    testUser = models.BooleanField(default=False)
    guestUser = models.BooleanField(default=False)
    validEmail = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    privilege_level = models.PositiveIntegerField(
        default=10000, verbose_name=_("Nivel de previlegios")
    )


    @property
    def is_operator(self):
        return (settings.SUPER_USER_MAX_LEVEL < self.privilege_level <= settings.OPERATOR_USER_MAX_LEVEL )

    @property
    def is_rootuser(self):
        return (self.privilege_level <= settings.SUPER_USER_MAX_LEVEL)

    is_test_account = models.BooleanField(
        default=False,
        verbose_name=_("Testing Account"),
        help_text=_("Test Account will be deleted every 10mins"),
    )

    def transformModel(self):
        if len(self.first_name.strip()) < 2:
            self.first_name = f"{self.username}"

        if len(self.last_name.strip()) < 2:
            self.last_name = "Last Name"

        if len(self.email.strip()) < 10:
            self.email = f"{self.username}_{datetime.now().timestamp()}@domain.com"
        return self

    @property
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return "/static/icons/user.png"

    @property
    def fullName(self):
        return self.get_full_name()

    @property
    def label(self):
        return self.fullName

    def syncAccount(self):
        pass

    def getSSOToken(self):
        token = default_token_generator.make_token(self)
        uidb64 = urlsafe_base64_encode(str(self.pk).encode())
        return {"token": token, "uidb64": uidb64}

    def getSessionToken(self):
        token = default_token_generator.make_token(self)
        uidb64 = urlsafe_base64_encode(str(self.pk).encode())
        return {"token": token, "uidb64": uidb64}

    @property
    def servidores(self):
        return []

    @property
    def app_settings(self):
        return {}

    @property
    def authToken(self):
        token = None
        try:
            token = Token.objects._or_create(user=self)
        except Exception:
            pass


        return token.key

    @property
    def token(self):
        return self.authToken

    @property
    def model_name(self):
        return self._meta.model_name

    @property
    def account_prefix(self):
        return "Account"

    @property
    def label(self):
        return f"{self.fullName}"

    class Meta(BaseModel.Meta):
        verbose_name = _("Account Record")
        verbose_name_plural = _("Account Collection")

    def __str__(self):
        return self.label
