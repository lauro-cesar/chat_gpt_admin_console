import os
import base64
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.db import close_old_connections

from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack
from django.utils.translation import gettext_lazy as _
import re
import json
import urllib.parse
from channels.auth import AuthMiddlewareStack
import itertools
from django.urls import path, include, re_path


class AnonymousUserAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        user = AnonymousUser()

        if user is not None:
            scope["user"] = user
            close_old_connections()

        return await self.app(scope, receive, send)


application = ProtocolTypeRouter(
    {"websocket": AnonymousUserAuthMiddleware(AuthMiddlewareStack(URLRouter()))}
)
