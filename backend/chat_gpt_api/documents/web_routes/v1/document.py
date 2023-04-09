
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include, re_path
from documents.views import DocumentTemplateView,DocumentDetailView, DocumentListView, DocumentUpdateView, DocumentDeleteView, DocumentCreateView

urlpatterns = [    
    path("", DocumentTemplateView.as_view(), name="document-index"),    
    path("collection/", DocumentListView.as_view(), name="document-list"),
    path("collection/<int:pk>/", DocumentDetailView.as_view(), name='document-detail'),
    path("collection/<int:pk>/editar/", DocumentUpdateView.as_view(), name='document-update'),
    path("collection/<int:pk>/remover/", DocumentDeleteView.as_view(), name='document-delete'),    
    path("collection/adicionar/", DocumentCreateView.as_view(), name='document-create'),
]