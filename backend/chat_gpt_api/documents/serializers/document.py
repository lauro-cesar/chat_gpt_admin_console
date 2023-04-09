
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import serializers
from documents.models import Document
from project.base_serializers import BaseSerializer


class DocumentIdOnlySerializer(BaseSerializer):
    class Meta:
        model = Document
        fields = ['id']
        if Document.READ_ONLY_FIELDS:
            read_only_fields =Document.READ_ONLY_FIELDS
            

class DocumentSerializer(BaseSerializer):
    class Meta:
        model = Document
        fields = Document.SERIALIZABLES
        if Document.READ_ONLY_FIELDS:
            read_only_fields =Document.READ_ONLY_FIELDS

class SerialDocumentSerializer(BaseSerializer):
    class Meta:
        model = Document
        fields = ["serial"]
        if Document.READ_ONLY_FIELDS:
            read_only_fields =Document.READ_ONLY_FIELDS
            