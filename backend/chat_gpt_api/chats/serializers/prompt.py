
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import serializers
from chats.models import Prompt
from project.base_serializers import BaseSerializer


class PromptIdOnlySerializer(BaseSerializer):
    class Meta:
        model = Prompt
        fields = ['id']
        if Prompt.READ_ONLY_FIELDS:
            read_only_fields =Prompt.READ_ONLY_FIELDS
            

class PromptSerializer(BaseSerializer):
    class Meta:
        model = Prompt
        fields = Prompt.SERIALIZABLES
        if Prompt.READ_ONLY_FIELDS:
            read_only_fields =Prompt.READ_ONLY_FIELDS

class SerialPromptSerializer(BaseSerializer):
    class Meta:
        model = Prompt
        fields = ["serial"]
        if Prompt.READ_ONLY_FIELDS:
            read_only_fields =Prompt.READ_ONLY_FIELDS
            