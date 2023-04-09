
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include, re_path
from chats.views import PromptTemplateTemplateView,PromptTemplateDetailView, PromptTemplateListView, PromptTemplateUpdateView, PromptTemplateDeleteView, PromptTemplateCreateView

urlpatterns = [    
    path("", PromptTemplateTemplateView.as_view(), name="prompttemplate-index"),    
    path("collection/", PromptTemplateListView.as_view(), name="prompttemplate-list"),
    path("collection/<int:pk>/", PromptTemplateDetailView.as_view(), name='prompttemplate-detail'),
    path("collection/<int:pk>/editar/", PromptTemplateUpdateView.as_view(), name='prompttemplate-update'),
    path("collection/<int:pk>/remover/", PromptTemplateDeleteView.as_view(), name='prompttemplate-delete'),    
    path("collection/adicionar/", PromptTemplateCreateView.as_view(), name='prompttemplate-create'),
]