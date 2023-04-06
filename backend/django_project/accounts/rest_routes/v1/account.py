from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from accounts.views import AccountViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r"account", AccountViewSet, basename="account")

urlpatterns = [path("", include(router.urls))]
