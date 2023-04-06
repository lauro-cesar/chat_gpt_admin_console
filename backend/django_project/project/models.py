"""
"""

from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import requests
from bs4 import BeautifulSoup
import re
from decimal import Decimal
from django_pandas.managers import DataFrameManager
from django.urls import reverse
from django.contrib import messages, admin
from django.utils.safestring import mark_safe
from django.contrib import messages, admin
from PIL import Image, ImageOps, ImageDraw, ImageFont
from io import BytesIO
import os
from django.utils.encoding import smart_str
import base64
import logging

logger = logging.getLogger(__name__)


def get_upload_to_path(instance, filename):
    return f"originais/{instance.model_name}"


class ModelBaseClass(models.Model):
    @property
    def getMeta(self):
        return self._meta

    @property
    def model_name(self):
        return self._meta.model_name

    @property
    def model_app_label(self):
        return self._meta.label

    def getReverseUrl(self, routeName, args=None):
        try:
            if args:
                route = reverse(f"{self.model_name}-{routeName}", args=args)
            else:
                route = reverse(f"{self.model_name}-{routeName}")

        except Exception as e:
            logger.error(e.__repr__())
            route = "/"
        return route

    def get_list_url(self):
        return self.getReverseUrl("list")

    def get_absolute_url(self):
        return self.getReverseUrl("detail", args=[str(self.id)])

    def get_delete_url(self):
        return self.getReverseUrl("delete", args=[str(self.id)])

    def get_detail_url(self):
        return self.getReverseUrl("detail", args=[str(self.id)])

    def get_create_url(self):
        return self.getReverseUrl("create")

    def get_update_url(self):
        return self.getReverseUrl("detail", args=[str(self.id)])

        # return reverse(f"{self._meta.model_name}-update", )

    class Meta:
        abstract = True


class BaseImageMedia(ModelBaseClass):
    media_original = models.ImageField(
        upload_to=get_upload_to_path,
        verbose_name=_(f"Original file"),
        default="default_icon.png",
    )
    original_raw_data = models.TextField(default="", blank=True)
    original_raw_data_ready = models.BooleanField(default=False)

    @property
    @admin.display(description="File Exist")
    def original_exists(self):
        return os.path.exists(self.media_original.path)

    @property
    @admin.display(description=_("Original Exif data"))
    def image_exif(self):
        im = Image.open(self.media_original)
        data = {}
        try:
            data = im.getexif().__dict__.get("_info", {}).__dict__
        except Exception as e:
            logger.error(e.__repr__())
            data = {}

        response = mark_safe(
            f"""<textarea>
                {data}
                </textarea>"""
        )

        im.close()
        return response

    @property
    @admin.display(
        ordering="created",
        description=_("Original Icon"),
    )
    def image_preview(self):
        return mark_safe(f"""<img width=128px src={self.image_preview_url}>""")

    @property
    @admin.display(
        ordering="created",
        description=_("Original preview"),
    )
    def imagem_link(self):
        return mark_safe(
            f"""<a href={self.image_preview_url}><img width=128px src={self.image_preview_url}></a>"""
        )

    @property
    @admin.display(
        ordering="created",
        description=_("Original url"),
    )
    def imagem_detail_url(self):
        try:
            url = self.get_detail_url()
        except Exception as e:
            logger.error(e.__repr__())
            url = "/static/imagens/default.png"
        return url

    @property
    @admin.display(
        ordering="created",
        description="Url relativa",
    )
    def image_preview_url(self):
        try:
            url = reverse(f"{self.model_name}-detail", args=[str(self.id)])
        except Exception as e:
            logger.error(e.__repr__())
            url = "/static/imagens/default.png"
        return url

    def getRawData(self, *args, **kwargs):
        im = Image.open(self.media_original)
        largura = kwargs.get("width", im.width)
        altura = kwargs.get("height", im.height)
        im = im.resize((largura, altura), Image.ANTIALIAS)
        buffered = BytesIO()
        im.save(buffered, format="PNG")
        imagem_raw_data = smart_str(base64.b64encode(buffered.getvalue()))
        im.close()
        return imagem_raw_data

    class Meta:
        abstract = True


class BaseModelForeignMixin:
    class Meta:
        abstract = True

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="criado_por_%(app_label)s_%(class)s_related",
        related_query_name="criado_por_%(app_label)s_%(class)ss",
    )

    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="modificado_por_%(app_label)s_%(class)s_related",
        related_query_name="modificado_por_%(app_label)s_%(class)ss",
    )

    removido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="removido_por_%(app_label)s_%(class)s_related",
        related_query_name="removido_por_%(app_label)s_%(class)ss",
    )

    belongs_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="belongs_to_%(app_label)s_%(class)s_related",
        related_query_name="belongs_to_%(app_label)s_%(class)ss",
    )


# Be careful with related_name and related_query_name. Why?
class BaseModelMixin(ModelBaseClass):
    class Meta:
        abstract = True

    FLUTTER_TYPES = {"id": {"type": "int"}}
    objects = DataFrameManager()
    dateCreated = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Data de criação")
    )
    lastModified = models.DateTimeField(
        auto_now=True, verbose_name=_("Última modificacao")
    )

    @property
    def serial(self):
        return self.lastModified.timestamp()

    isActive = models.BooleanField(default=True, null=True)
    isPublic = models.BooleanField(default=False, null=True)
    isRemoved = models.BooleanField(default=False, null=True)

    def transformModel(self):
        return self

    @property
    def get_rest_endpoint(self):
        try:
            if hasattr(self, "REST_BASENAME"):
                return reverse(f"{self.REST_BASENAME}-list")
            return reverse(f"{self._meta.model_name}-list")
        except Exception as e:
            logger.error(e.__repr__())
            return "/"

    @property
    @admin.display(
        ordering="dateCreated",
        description="Rest Endpoint",
    )
    def rest_endpoint(self):
        return mark_safe(f"""<a href={self.get_rest_endpoint}{self.id}.json>REST</a>""")

    @classmethod
    def propriedades(cls):
        return list(map(lambda f: f.name, cls._meta.fields))

    @classmethod
    def get_or_none(cls, *args, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except Exception as e:
            logger.error(e.__repr__())
            return None

    def coord_from_address(self, address):
        try:
            url = f"http://45.56.102.198:8181/search.php?address={address}&format=json"
            return requests.get(url, timeout=20).json()
        except Exception as e:
            logger.error(e.__repr__())
            return [{}]

    def reverse_address_from_postal_code(self, postalcode):
        try:
            url = f"http://45.56.102.198:8181/search.php?postalcode={postalcode}&format=json"
            return requests.get(url, timeout=20).json()
        except Exception as e:
            logger.error(e.__repr__())
            return [{}]


class BaseModel(BaseModelMixin, BaseModelForeignMixin):
    class Meta:
        abstract = True
        ordering = ["lastModified"]


class StackedModel(BaseModel):
    stackOrder = models.FloatField(default=100, verbose_name=_("Ordem de exibição"))

    class Meta(BaseModel.Meta):
        abstract = True
        ordering = ["stackOrder"]
