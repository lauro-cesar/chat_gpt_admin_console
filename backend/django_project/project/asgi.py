import os
import base64
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.db import close_old_connections
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.utils.translation import gettext_lazy as _
import re
import json
import urllib.parse
from channels.auth import AuthMiddlewareStack
import itertools
from django.urls import path, include, re_path

isToken = re.compile(r"""(?<=Token )(.*)""", re.IGNORECASE)
isBasic = re.compile(r"""(?<=Basic )(.*)""", re.IGNORECASE)
isBearer = re.compile(r"""(?<=Bearer )(.*)""", re.IGNORECASE)


@database_sync_to_async
def get_user_by_password(scope, username, password):
    return authenticate(scope, username=username, password=password)


@database_sync_to_async
def get_user_by_token(token):
    user = AnonymousUser()

    try:
        tokenUser = Token.objects.select_related("user").get(key=token)
    except Token.DoesNotExist:
        raise exceptions.AuthenticationFailed(_("Invalid token."))
    else:
        user = tokenUser.user

    if not user.is_active:
        raise exceptions.AuthenticationFailed(_("User inactive or deleted."))
    return user


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        user = None
        headers = dict(scope["headers"])
        query_string = dict(
            urllib.parse.parse_qsl(scope.get("query_string", "").decode())
        )

        sso_token = query_string.get("sso", None)

        if sso_token:
            user = await get_user_by_token(sso_token)

        # TODO: Implement a context manager here

        if user is None:
            if b"authorization" in headers:
                if isToken.search(headers[b"authorization"].decode()):
                    user = await get_user_by_token(
                        isToken.search(headers[b"authorization"].decode()).group(0)
                    )

                if isBearer.search(headers[b"authorization"].decode()):
                    user = await get_user_by_token(
                        isBearer.search(headers[b"authorization"].decode()).group(0)
                    )

                if isBasic.search(headers[b"authorization"].decode()):
                    credentials = isBasic.search(
                        headers[b"authorization"].decode()
                    ).group(0)
                    try:
                        inputInfo = base64.b64decode(credentials)
                        username, password = inputInfo.decode().split(":")
                        user = await get_user_by_password(
                            scope, username=username, password=password
                        )
                    except Exception as e:
                        print(e.__repr__())

        if user is not None:
            scope["user"] = user
            close_old_connections()

        return await self.app(scope, receive, send)


application = ProtocolTypeRouter(
    {
        "websocket": TokenAuthMiddleware(
            AuthMiddlewareStack(
                URLRouter(
                    # list(boletos_router)
                )
            )
        )
    }
)
