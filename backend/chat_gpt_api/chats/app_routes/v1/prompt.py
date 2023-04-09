
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path,include, re_path
from chats.views import PromptTemplateView,PromptDetailView, PromptListView, PromptUpdateView, PromptDeleteView, PromptCreateView

urlpatterns = [    
    path("", PromptTemplateView.as_view(template_name="prompt/app_templates/v1/prompt_index.html"), name="prompt-index"),
    path("collection/", PromptListView.as_view(template_name = "prompt/app_templates/v1/prompt_list.html"), name="prompt-list"),
    path("collection/<int:pk>/", PromptDetailView.as_view(template_name = "prompt/app_templates/v1/prompt_detail.html"), name='prompt-detail'),
    path("collection/<int:pk>/editar/", PromptUpdateView.as_view(template_name = "prompt/app_templates/v1/prompt_update.html"), name='prompt-update'),
    path("collection/<int:pk>/remover/", PromptDeleteView.as_view(template_name = "prompt/app_templates/v1/prompt_delete.html"), name='prompt-delete'),    path("collection/adicionar/", PromptCreateView.as_view(template_name = "prompt/app_templates/v1/prompt_create.html"), name='prompt-create'),
]