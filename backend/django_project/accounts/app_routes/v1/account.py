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

urlpatterns = [
    path(
        "",
        AccountTemplateView.as_view(
            template_name="account/app_templates/v1/account_index.html"
        ),
        name="account-index",
    ),
    path(
        "collection/",
        AccountListView.as_view(
            template_name="account/app_templates/v1/account_list.html"
        ),
        name="account-list",
    ),
    path(
        "collection/<int:pk>/",
        AccountDetailView.as_view(
            template_name="account/app_templates/v1/account_detail.html"
        ),
        name="account-detail",
    ),
    path(
        "collection/<int:pk>/editar/",
        AccountUpdateView.as_view(
            template_name="account/app_templates/v1/account_update.html"
        ),
        name="account-update",
    ),
    path(
        "collection/<int:pk>/remover/",
        AccountDeleteView.as_view(
            template_name="account/app_templates/v1/account_delete.html"
        ),
        name="account-delete",
    ),
    path(
        "collection/adicionar/",
        AccountCreateView.as_view(
            template_name="account/app_templates/v1/account_create.html"
        ),
        name="account-create",
    ),
]
