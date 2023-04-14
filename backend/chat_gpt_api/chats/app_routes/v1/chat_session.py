
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path,include, re_path
from chats.views import ChatSessionTemplateView,ChatSessionDetailView, ChatSessionListView, ChatSessionUpdateView, ChatSessionDeleteView, ChatSessionCreateView

urlpatterns = [    
    path("", ChatSessionTemplateView.as_view(template_name="chatsession/app_templates/v1/chatsession_index.html"), name="chatsession-index"),
    path("collection/", ChatSessionListView.as_view(template_name = "chatsession/app_templates/v1/chatsession_list.html"), name="chatsession-list"),
    path("collection/<int:pk>/", ChatSessionDetailView.as_view(template_name = "chatsession/app_templates/v1/chatsession_detail.html"), name='chatsession-detail'),
    path("collection/<int:pk>/editar/", ChatSessionUpdateView.as_view(template_name = "chatsession/app_templates/v1/chatsession_update.html"), name='chatsession-update'),
    path("collection/<int:pk>/remover/", ChatSessionDeleteView.as_view(template_name = "chatsession/app_templates/v1/chatsession_delete.html"), name='chatsession-delete'),    path("collection/adicionar/", ChatSessionCreateView.as_view(template_name = "chatsession/app_templates/v1/chatsession_create.html"), name='chatsession-create'),
]