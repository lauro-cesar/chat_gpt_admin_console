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
from project.models import BaseModel, StackedModel, BaseModelMixin
from django.contrib.auth.models import AbstractUser, User, PermissionsMixin, Group, Permission


class AccountType(BaseModelMixin):
    MODEL_LIST_ORDER_VALUE = 0
    SERIALIZABLES = ["id", "label", "serial"]
    FLUTTER_TYPES = {
        "default": "String",
        "id": "int",
    }
    FLUTTER_MANY_TO_MANY = {}
    FLUTTER_ONE_TO_ONE = {}
    READ_ONLY_FIELDS = ["id", "serial"]
    ADMIN_LIST_EDITABLE = ["privilege_level"]
    ADMIN_LIST_DISPLAY = ["label", "privilege_level"]
    ADMIN_ORDERING = []
    ADMIN_FILTER_HORIZONTAL = ["groups", "account_type_permissions"]
    ADMIN_LIST_FILTER = []
    ADMIN_SEARCH_FILTER = []
    ADMIN_DISPLAY_LINKS = []
    EXCLUDE_FROM_ADMIN = []
    CREATE_FIELDS = []
    FORM_FIELDS = []
    REST_BASENAME = "accounttype"

    TASKS = {"on_create": [], "on_save": [], "on_delete": []}
    account_type = models.CharField(max_length=128, verbose_name=_("Tipo de conta"))
    privilege_level = models.PositiveIntegerField(
        default=10000, verbose_name=_("Nivel de previlegios")
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_account_type_set",
        related_query_name="user_account_type",
    )

    account_type_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("Account Type permissions"),
        blank=True,
        help_text=_("Specific permissions for this Account Type."),
        related_name="account_type_permission_set",
        related_query_name="account_type_permission",
    )

    @property
    def label(self):
        return self.account_type

    class Meta(BaseModel.Meta):
        verbose_name = _("Account previlege level")
        verbose_name_plural = _("Account previlegies level")

    def __str__(self):
        return self.label
