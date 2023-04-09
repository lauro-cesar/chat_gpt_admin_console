
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import serializers
from chats.models import Answer
from project.base_serializers import BaseSerializer


class AnswerIdOnlySerializer(BaseSerializer):
    class Meta:
        model = Answer
        fields = ['id']
        if Answer.READ_ONLY_FIELDS:
            read_only_fields =Answer.READ_ONLY_FIELDS
            

class AnswerSerializer(BaseSerializer):
    class Meta:
        model = Answer
        fields = Answer.SERIALIZABLES
        if Answer.READ_ONLY_FIELDS:
            read_only_fields =Answer.READ_ONLY_FIELDS

class SerialAnswerSerializer(BaseSerializer):
    class Meta:
        model = Answer
        fields = ["serial"]
        if Answer.READ_ONLY_FIELDS:
            read_only_fields =Answer.READ_ONLY_FIELDS
            