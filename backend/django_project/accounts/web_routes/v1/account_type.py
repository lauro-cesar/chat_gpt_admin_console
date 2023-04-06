from django.urls import path, include, re_path
from accounts.views import (
    AccountTypeTemplateView,
    AccountTypeDetailView,
    AccountTypeListView,
    AccountTypeUpdateView,
    AccountTypeDeleteView,
    AccountTypeCreateView,
)

urlpatterns = [
    path("", AccountTypeTemplateView.as_view(), name="accounttype-index"),
    path("collection/", AccountTypeListView.as_view(), name="accounttype-list"),
    path(
        "collection/<int:pk>/",
        AccountTypeDetailView.as_view(),
        name="accounttype-detail",
    ),
    path(
        "collection/<int:pk>/editar/",
        AccountTypeUpdateView.as_view(),
        name="accounttype-update",
    ),
    path(
        "collection/<int:pk>/remover/",
        AccountTypeDeleteView.as_view(),
        name="accounttype-delete",
    ),
    path(
        "collection/adicionar/",
        AccountTypeCreateView.as_view(),
        name="accounttype-create",
    ),
]
