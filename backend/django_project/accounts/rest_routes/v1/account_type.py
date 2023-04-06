from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from accounts.views import (
    AccountTypeViewSet,
    SerialAccountTypeViewSet,
    AccountTypeIdOnlyViewSet,
)
from django.conf import settings

router = DefaultRouter()

router.register(r"accounttype", AccountTypeViewSet, basename="accounttype")
router.register(
    r"serial-accounttype", SerialAccountTypeViewSet, basename="serial-accounttype"
)
router.register(
    r"accounttype-collection-id-only",
    AccountTypeIdOnlyViewSet,
    basename="id-only-accounttype",
)

urlpatterns = [path("", include(router.urls))]
