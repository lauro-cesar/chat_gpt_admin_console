"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path, include, re_path
from accounts.views import (
    AccountTemplateView,
    AccountDetailView,
    AccountListView,
    AccountUpdateView,
    AccountDeleteView,
    AccountCreateView,
)
from accounts.forms import UserCreateForm, DeveloperCreateForm, GamerCreateForm


urlpatterns = [
    path("", AccountTemplateView.as_view(), name="account-index"),
    path("collection/", AccountListView.as_view(), name="account-list"),
    path("collection/<int:pk>/", AccountDetailView.as_view(), name="account-detail"),
    path(
        "collection/<int:pk>/editar/",
        AccountUpdateView.as_view(),
        name="account-update",
    ),
    path(
        "collection/<int:pk>/remover/",
        AccountDeleteView.as_view(),
        name="account-delete",
    ),
    path(
        "collection/adicionar/",
        AccountCreateView.as_view(form_class=UserCreateForm),
        name="account-create",
    ),
    path(
        "collection/adicionar/developer/",
        AccountCreateView.as_view(form_class=DeveloperCreateForm),
        name="developer-account-create",
    ),
    path(
        "collection/adicionar/gamer/",
        AccountCreateView.as_view(form_class=GamerCreateForm),
        name="gamer-account-create",
    ),
]
