from django.contrib import admin
from django.urls import path, re_path, include, converters
from django.conf import settings
from .views import CustomAuthToken
from .admin import ProjectAdminSite, project_dashboard_site, project_admin_site


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "console/",
        include(
            [
                path(
                    "admin/",
                    include(
                        [
                            path("", project_admin_site.urls),
                        ]
                    ),
                ),
                path("manager/", project_dashboard_site.urls),
            ]
        ),
    ),
    path(
        "web-api/v1/",
        include(
            [
                path(
                    "accounts/",
                    include(
                        [
                            path("app/", include("accounts.web_routes.v1.account")),
                            path("", include("django.contrib.auth.urls")),
                        ]
                    ),
                ),
            ]
        ),
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("django.contrib.flatpages.urls")),
]
