from django.utils.deprecation import MiddlewareMixin
from django.contrib import auth
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect


class RestSSOAuthMiddleWare:
    def get_user(self, request):
        if not hasattr(request, "_cached_user"):
            request._cached_user = auth.get_user(request)
        return request._cached_user

    def __init__(self, get_response):
        self.get_response = get_response

    def isAdminConsole(self, request):
        return request.path.startswith("/console/admin/")

    def isSuperUser(self, request):
        return request.user.is_superuser

    def __call__(self, request, *arg, **kwargs):
        response = None
        print(kwargs)
        print("ARgs no middle")

        # if request.user.is_authenticated:
        #     if self.isAdminConsole(request):
        #         if self.isSuperUser(request):
        #             response = self.get_response(request)
        #         else:
        #             response = HttpResponseRedirect(redirect_to="/console/developer/")

        if response is None:
            response = self.get_response(request)
        else:
            response = self.get_response(request)
        return response
