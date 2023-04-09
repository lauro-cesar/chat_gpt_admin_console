from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        criado_por = self.context.get("criado_por", None)
        if criado_por:
            validated_data.update({"criado_por": criado_por})
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        modificado_por = self.context.get("modificado_por", None)
        if modificado_por:
            validated_data.update({"modificado_por": modificado_por})
        instance = super().update(instance, validated_data)
        return instance
