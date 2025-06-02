from rest_framework import serializers
from bson import ObjectId
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

@extend_schema_field(OpenApiTypes.STR)
class ObjectIdField(serializers.Field):
    """Campo personalizado para ObjectId do MongoDB"""
    
    def to_representation(self, value):
        if not ObjectId.is_valid(value):
            return None
        return str(value)

    def to_internal_value(self, data):
        if not ObjectId.is_valid(data):
            raise serializers.ValidationError(
                'ID inválido'
            )
        return ObjectId(data) 