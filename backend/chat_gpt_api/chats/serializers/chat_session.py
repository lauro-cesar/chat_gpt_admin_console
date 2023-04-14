
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import serializers
from chats.models import ChatSession
from project.base_serializers import BaseSerializer


class ChatSessionIdOnlySerializer(BaseSerializer):
    class Meta:
        model = ChatSession
        fields = ['id']
        if ChatSession.READ_ONLY_FIELDS:
            read_only_fields =ChatSession.READ_ONLY_FIELDS
            

class ChatSessionSerializer(BaseSerializer):
    class Meta:
        model = ChatSession
        fields = ChatSession.SERIALIZABLES
        if ChatSession.READ_ONLY_FIELDS:
            read_only_fields =ChatSession.READ_ONLY_FIELDS

class SerialChatSessionSerializer(BaseSerializer):
    class Meta:
        model = ChatSession
        fields = ["serial"]
        if ChatSession.READ_ONLY_FIELDS:
            read_only_fields =ChatSession.READ_ONLY_FIELDS
            