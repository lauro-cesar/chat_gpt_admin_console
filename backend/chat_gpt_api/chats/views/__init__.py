"""
Copyright (c) 2020, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from .prompt_template import (
    PromptTemplateTemplateView,
    PromptTemplateDetailView, 
    PromptTemplateListView, 
    PromptTemplateUpdateView, 
    PromptTemplateCreateView, 
    PromptTemplateDeleteView,
    SerialPromptTemplateViewSet,
    PromptTemplateIdOnlyViewSet,    
    PromptTemplateViewSet)

from .prompt import (
    PromptTemplateView,
    PromptDetailView, 
    PromptListView, 
    PromptUpdateView, 
    PromptCreateView, 
    PromptDeleteView,
    SerialPromptViewSet,
    PromptIdOnlyViewSet,    
    PromptViewSet)