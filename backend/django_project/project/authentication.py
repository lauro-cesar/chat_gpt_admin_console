from rest_framework.authentication import TokenAuthentication
import base64
import binascii

from django.contrib.auth import authenticate, get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from django.utils.translation import gettext_lazy as _

from rest_framework import HTTP_HEADER_ENCODING, exceptions


class APITokenAuthentication(TokenAuthentication):
    """
    Django rest uses Token keyword by default, extending TokenAuth and changed it to Bearer
    """

    keyword = "Bearer"

    def get_authorization_header(self, request):
        auth = request.META.get("HTTP_AUTHORIZATION", b"")
        if isinstance(auth, str):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def get_token_key(self, request):
        token = request.GET.get("SSO_TOKEN", None)
        if token:
            print(f"Tem token no REST: {token}")
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

    def authenticate(self, request):
        token_key = self.get_token_key(request)
        return self.authenticate_credentials(token_key)
