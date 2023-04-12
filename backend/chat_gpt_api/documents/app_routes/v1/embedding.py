
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path,include, re_path
from documents.views import EmbeddingTemplateView,EmbeddingDetailView, EmbeddingListView, EmbeddingUpdateView, EmbeddingDeleteView, EmbeddingCreateView

urlpatterns = [    
    path("", EmbeddingTemplateView.as_view(template_name="embedding/app_templates/v1/embedding_index.html"), name="embedding-index"),
    path("collection/", EmbeddingListView.as_view(template_name = "embedding/app_templates/v1/embedding_list.html"), name="embedding-list"),
    path("collection/<int:pk>/", EmbeddingDetailView.as_view(template_name = "embedding/app_templates/v1/embedding_detail.html"), name='embedding-detail'),
    path("collection/<int:pk>/editar/", EmbeddingUpdateView.as_view(template_name = "embedding/app_templates/v1/embedding_update.html"), name='embedding-update'),
    path("collection/<int:pk>/remover/", EmbeddingDeleteView.as_view(template_name = "embedding/app_templates/v1/embedding_delete.html"), name='embedding-delete'),    path("collection/adicionar/", EmbeddingCreateView.as_view(template_name = "embedding/app_templates/v1/embedding_create.html"), name='embedding-create'),
]