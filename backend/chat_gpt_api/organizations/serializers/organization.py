
"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import serializers
from organizations.models import Organization
from project.base_serializers import BaseSerializer


class OrganizationIdOnlySerializer(BaseSerializer):
    class Meta:
        model = Organization
        fields = ['id']
        if Organization.READ_ONLY_FIELDS:
            read_only_fields =Organization.READ_ONLY_FIELDS
            

class OrganizationSerializer(BaseSerializer):
    class Meta:
        model = Organization
        fields = Organization.SERIALIZABLES
        if Organization.READ_ONLY_FIELDS:
            read_only_fields =Organization.READ_ONLY_FIELDS

class SerialOrganizationSerializer(BaseSerializer):
    class Meta:
        model = Organization
        fields = ["serial"]
        if Organization.READ_ONLY_FIELDS:
            read_only_fields =Organization.READ_ONLY_FIELDS
            