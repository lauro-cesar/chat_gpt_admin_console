"""[summary]

[description]
"""
from django.contrib.auth import authenticate
from django.utils.deprecation import MiddlewareMixin

from django.utils.functional import SimpleLazyObject
from django.contrib.auth import get_user_model
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from django.contrib import auth
from django.http import JsonResponse
from rest_framework import status

User = get_user_model()


class SSOAuthMiddleWare(MiddlewareMixin):
    def get_user(self, request):
        if not hasattr(request, "_cached_user"):
            request._cached_user = auth.get_user(request)
        return request._cached_user

    def get_authorization_header(self, request):
        auth = request.META.get("HTTP_AUTHORIZATION", b"")
        if isinstance(auth, str):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def get_token_key(self, request):
        token = request.GET.get("SSO_TOKEN", None)
        if token:
            print(f"Tem token: {token}")
            return token

        authCheck = self.get_authorization_header(request).split()
        if len(authCheck) > 1:
            try:
                key = authCheck[1].decode()
            except UnicodeError:
                msg = _(
                    "Invalid token header. Token string should not contain invalid characters."
                )
                raise exceptions.AuthenticationFailed(msg)
            else:
                return key

        return None

    def process_request(
        self,
        request,
    ):
        # print(kwargs.keys())
        assert hasattr(request, "session"), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )

        token_key = self.get_token_key(request)

        if token_key:
            print(f"Verificando auth com token: {token_key}")
            try:
                token = Token.objects.select_related("user").get(key=token_key)
            except Token.DoesNotExist:
                print("Token nao existe?")
                return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)
                # raise exceptions.AuthenticationFailed(_("Invalid token."))
            else:
                print("Token exist?")
                if not token.user.is_active:
                    print("User inativo")
                    return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)
                    # raise exceptions.AuthenticationFailed(_("User inactive or deleted."))

                if not hasattr(request, "_cached_user"):
                    request.user = token.user
                    auth.login(request, token.user)
                    print("Nao tem cache de user")
                    request._cached_user = token.user

                request.user = request._cached_user
