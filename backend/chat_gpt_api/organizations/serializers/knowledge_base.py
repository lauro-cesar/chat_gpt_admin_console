
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import serializers
from organizations.models import KnowledgeBase
from project.base_serializers import BaseSerializer


class KnowledgeBaseIdOnlySerializer(BaseSerializer):
    class Meta:
        model = KnowledgeBase
        fields = ['id']
        if KnowledgeBase.READ_ONLY_FIELDS:
            read_only_fields =KnowledgeBase.READ_ONLY_FIELDS
            

class KnowledgeBaseSerializer(BaseSerializer):
    class Meta:
        model = KnowledgeBase
        fields = KnowledgeBase.SERIALIZABLES
        if KnowledgeBase.READ_ONLY_FIELDS:
            read_only_fields =KnowledgeBase.READ_ONLY_FIELDS

class SerialKnowledgeBaseSerializer(BaseSerializer):
    class Meta:
        model = KnowledgeBase
        fields = ["serial"]
        if KnowledgeBase.READ_ONLY_FIELDS:
            read_only_fields =KnowledgeBase.READ_ONLY_FIELDS
            