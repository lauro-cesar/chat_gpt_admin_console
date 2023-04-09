
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from django.urls import path,include, re_path
from chats.views import AnswerTemplateView,AnswerDetailView, AnswerListView, AnswerUpdateView, AnswerDeleteView, AnswerCreateView

urlpatterns = [    
    path("", AnswerTemplateView.as_view(template_name="answer/app_templates/v1/answer_index.html"), name="answer-index"),
    path("collection/", AnswerListView.as_view(template_name = "answer/app_templates/v1/answer_list.html"), name="answer-list"),
    path("collection/<int:pk>/", AnswerDetailView.as_view(template_name = "answer/app_templates/v1/answer_detail.html"), name='answer-detail'),
    path("collection/<int:pk>/editar/", AnswerUpdateView.as_view(template_name = "answer/app_templates/v1/answer_update.html"), name='answer-update'),
    path("collection/<int:pk>/remover/", AnswerDeleteView.as_view(template_name = "answer/app_templates/v1/answer_delete.html"), name='answer-delete'),    path("collection/adicionar/", AnswerCreateView.as_view(template_name = "answer/app_templates/v1/answer_create.html"), name='answer-create'),
]