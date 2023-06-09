"""
Copyright (c) 2020, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""

from .document import (
    DocumentTemplateView,
    DocumentDetailView, 
    DocumentListView, 
    DocumentUpdateView, 
    DocumentCreateView, 
    DocumentDeleteView,
    SerialDocumentViewSet,
    DocumentIdOnlyViewSet,    
    DocumentViewSet)
from .embedding import (
    EmbeddingTemplateView,
    EmbeddingDetailView, 
    EmbeddingListView, 
    EmbeddingUpdateView, 
    EmbeddingCreateView, 
    EmbeddingDeleteView,
    SerialEmbeddingViewSet,
    EmbeddingIdOnlyViewSet,    
    EmbeddingViewSet)