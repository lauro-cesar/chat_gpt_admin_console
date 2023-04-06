"""
Copyright (c) 2023, Lauro Cesar <lauro@hostcert.com.br>
All rights reserved under BSD 3-Clause License.
"""
from rest_framework import serializers
from accounts.models import Account
from project.base_serializers import BaseSerializer


class AccountSerializer(BaseSerializer):
    class Meta:
        model = Account
        fields = Account.SERIALIZABLES
        if Account.READ_ONLY_FIELDS:
            read_only_fields = Account.READ_ONLY_FIELDS
