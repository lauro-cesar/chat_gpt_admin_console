
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import serializers
from chats.models import Question
from project.base_serializers import BaseSerializer


class QuestionIdOnlySerializer(BaseSerializer):
    class Meta:
        model = Question
        fields = ['id']
        if Question.READ_ONLY_FIELDS:
            read_only_fields =Question.READ_ONLY_FIELDS
            

class QuestionSerializer(BaseSerializer):
    class Meta:
        model = Question
        fields = Question.SERIALIZABLES
        if Question.READ_ONLY_FIELDS:
            read_only_fields =Question.READ_ONLY_FIELDS

class SerialQuestionSerializer(BaseSerializer):
    class Meta:
        model = Question
        fields = ["serial"]
        if Question.READ_ONLY_FIELDS:
            read_only_fields =Question.READ_ONLY_FIELDS
            