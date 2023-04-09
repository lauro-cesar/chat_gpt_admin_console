
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import serializers
from chats.models import PromptTemplate
from project.base_serializers import BaseSerializer


class PromptTemplateIdOnlySerializer(BaseSerializer):
    class Meta:
        model = PromptTemplate
        fields = ['id']
        if PromptTemplate.READ_ONLY_FIELDS:
            read_only_fields =PromptTemplate.READ_ONLY_FIELDS
            

class PromptTemplateSerializer(BaseSerializer):
    class Meta:
        model = PromptTemplate
        fields = PromptTemplate.SERIALIZABLES
        if PromptTemplate.READ_ONLY_FIELDS:
            read_only_fields =PromptTemplate.READ_ONLY_FIELDS

class SerialPromptTemplateSerializer(BaseSerializer):
    class Meta:
        model = PromptTemplate
        fields = ["serial"]
        if PromptTemplate.READ_ONLY_FIELDS:
            read_only_fields =PromptTemplate.READ_ONLY_FIELDS
            