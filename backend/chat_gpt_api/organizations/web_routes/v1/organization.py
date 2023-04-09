
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include, re_path
from organizations.views import OrganizationTemplateView,OrganizationDetailView, OrganizationListView, OrganizationUpdateView, OrganizationDeleteView, OrganizationCreateView

urlpatterns = [    
    path("", OrganizationTemplateView.as_view(), name="organization-index"),    
    path("collection/", OrganizationListView.as_view(), name="organization-list"),
    path("collection/<int:pk>/", OrganizationDetailView.as_view(), name='organization-detail'),
    path("collection/<int:pk>/editar/", OrganizationUpdateView.as_view(), name='organization-update'),
    path("collection/<int:pk>/remover/", OrganizationDeleteView.as_view(), name='organization-delete'),    
    path("collection/adicionar/", OrganizationCreateView.as_view(), name='organization-create'),
]