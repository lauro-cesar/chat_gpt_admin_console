
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include, re_path
from organizations.views import KnowledgeBaseTemplateView,KnowledgeBaseDetailView, KnowledgeBaseListView, KnowledgeBaseUpdateView, KnowledgeBaseDeleteView, KnowledgeBaseCreateView

urlpatterns = [    
    path("", KnowledgeBaseTemplateView.as_view(), name="knowledgebase-index"),    
    path("collection/", KnowledgeBaseListView.as_view(), name="knowledgebase-list"),
    path("collection/<int:pk>/", KnowledgeBaseDetailView.as_view(), name='knowledgebase-detail'),
    path("collection/<int:pk>/editar/", KnowledgeBaseUpdateView.as_view(), name='knowledgebase-update'),
    path("collection/<int:pk>/remover/", KnowledgeBaseDeleteView.as_view(), name='knowledgebase-delete'),    
    path("collection/adicionar/", KnowledgeBaseCreateView.as_view(), name='knowledgebase-create'),
]