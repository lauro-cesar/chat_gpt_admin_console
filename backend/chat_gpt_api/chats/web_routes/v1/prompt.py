
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include, re_path
from chats.views import PromptTemplateView,PromptDetailView, PromptListView, PromptUpdateView, PromptDeleteView, PromptCreateView

urlpatterns = [    
    path("", PromptTemplateView.as_view(), name="prompt-index"),    
    path("collection/", PromptListView.as_view(), name="prompt-list"),
    path("collection/<int:pk>/", PromptDetailView.as_view(), name='prompt-detail'),
    path("collection/<int:pk>/editar/", PromptUpdateView.as_view(), name='prompt-update'),
    path("collection/<int:pk>/remover/", PromptDeleteView.as_view(), name='prompt-delete'),    
    path("collection/adicionar/", PromptCreateView.as_view(), name='prompt-create'),
]