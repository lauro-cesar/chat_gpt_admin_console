
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from django.urls import path,include, re_path
from chats.views import QuestionTemplateView,QuestionDetailView, QuestionListView, QuestionUpdateView, QuestionDeleteView, QuestionCreateView

urlpatterns = [    
    path("", QuestionTemplateView.as_view(), name="question-index"),    
    path("collection/", QuestionListView.as_view(), name="question-list"),
    path("collection/<int:pk>/", QuestionDetailView.as_view(), name='question-detail'),
    path("collection/<int:pk>/editar/", QuestionUpdateView.as_view(), name='question-update'),
    path("collection/<int:pk>/remover/", QuestionDeleteView.as_view(), name='question-delete'),    
    path("collection/adicionar/", QuestionCreateView.as_view(), name='question-create'),
]