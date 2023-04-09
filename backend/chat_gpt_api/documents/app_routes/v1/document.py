
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path,include, re_path
from documents.views import DocumentTemplateView,DocumentDetailView, DocumentListView, DocumentUpdateView, DocumentDeleteView, DocumentCreateView

urlpatterns = [    
    path("", DocumentTemplateView.as_view(template_name="document/app_templates/v1/document_index.html"), name="document-index"),
    path("collection/", DocumentListView.as_view(template_name = "document/app_templates/v1/document_list.html"), name="document-list"),
    path("collection/<int:pk>/", DocumentDetailView.as_view(template_name = "document/app_templates/v1/document_detail.html"), name='document-detail'),
    path("collection/<int:pk>/editar/", DocumentUpdateView.as_view(template_name = "document/app_templates/v1/document_update.html"), name='document-update'),
    path("collection/<int:pk>/remover/", DocumentDeleteView.as_view(template_name = "document/app_templates/v1/document_delete.html"), name='document-delete'),    path("collection/adicionar/", DocumentCreateView.as_view(template_name = "document/app_templates/v1/document_create.html"), name='document-create'),
]