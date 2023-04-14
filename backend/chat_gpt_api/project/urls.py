from django.contrib import admin
from django.urls import path, re_path, include, converters
from django.conf import settings
from .views import CustomAuthToken
from .admin import ProjectAdminSite, project_dashboard_site, project_admin_site
from rest_framework.authtoken import views

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
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
        "rest-api/v1/",
        include(
            [
                path("", include("documents.rest_routes.v1.document")),
                path("", include("organizations.rest_routes.v1.organization")),
                path("", include("organizations.rest_routes.v1.knowledge_base")),
                path("", include("chats.rest_routes.v1.chat_session")),
                path("", include("chats.rest_routes.v1.prompt")),
                path("", include("chats.rest_routes.v1.question")),                
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
    path("", include("django.contrib.flatpages.urls")),
]
