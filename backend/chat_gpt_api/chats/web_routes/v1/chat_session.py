
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include, re_path
from chats.views import ChatSessionTemplateView,ChatSessionDetailView, ChatSessionListView, ChatSessionUpdateView, ChatSessionDeleteView, ChatSessionCreateView

urlpatterns = [    
    path("", ChatSessionTemplateView.as_view(), name="chatsession-index"),    
    path("collection/", ChatSessionListView.as_view(), name="chatsession-list"),
    path("collection/<int:pk>/", ChatSessionDetailView.as_view(), name='chatsession-detail'),
    path("collection/<int:pk>/editar/", ChatSessionUpdateView.as_view(), name='chatsession-update'),
    path("collection/<int:pk>/remover/", ChatSessionDeleteView.as_view(), name='chatsession-delete'),    
    path("collection/adicionar/", ChatSessionCreateView.as_view(), name='chatsession-create'),
]