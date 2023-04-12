
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import serializers
from documents.models import Embedding
from project.base_serializers import BaseSerializer


class EmbeddingIdOnlySerializer(BaseSerializer):
    class Meta:
        model = Embedding
        fields = ['id']
        if Embedding.READ_ONLY_FIELDS:
            read_only_fields =Embedding.READ_ONLY_FIELDS
            

class EmbeddingSerializer(BaseSerializer):
    class Meta:
        model = Embedding
        fields = Embedding.SERIALIZABLES
        if Embedding.READ_ONLY_FIELDS:
            read_only_fields =Embedding.READ_ONLY_FIELDS

class SerialEmbeddingSerializer(BaseSerializer):
    class Meta:
        model = Embedding
        fields = ["serial"]
        if Embedding.READ_ONLY_FIELDS:
            read_only_fields =Embedding.READ_ONLY_FIELDS
            