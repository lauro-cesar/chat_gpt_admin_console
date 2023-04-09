
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from organizations.views import OrganizationViewSet,SerialOrganizationViewSet, OrganizationIdOnlyViewSet
from django.conf import settings

router = DefaultRouter()

router.register(r'organization', OrganizationViewSet,basename="organization")
router.register(r'serial-organization', SerialOrganizationViewSet,basename="serial-organization")
router.register(r'organization-collection-id-only', OrganizationIdOnlyViewSet,basename="id-only-organization")

urlpatterns = [
	path('', include(router.urls))
]