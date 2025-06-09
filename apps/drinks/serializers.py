from rest_framework import serializers
from bson import ObjectId
from .models import (
    TipoIngrediente, TipoUtensilio, UnidadeMedida,
    PerfilSabor, Ingrediente, Utensilio, Drink
)
from .fields import ObjectIdField
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Tipo de Ingrediente',
            value={
                'nome': 'Destilado',
                'nome_en': 'Spirit',
                'ordem': 1
            }
        )
    ]
)
class TipoReferenciaSerializer(serializers.Serializer):
    _id = ObjectIdField(required=False)
    nome = serializers.CharField(max_length=100)
    nome_en = serializers.CharField(max_length=100)
    ordem = serializers.IntegerField(required=False)

    def create(self, validated_data):
        result = self.Meta.model.insert_one(validated_data)
        return self.Meta.model.find_one({'_id': result.inserted_id})

    def update(self, instance, validated_data):
        self.Meta.model.update_one(
            {'_id': instance['_id']},
            {'$set': validated_data}
        )
        return {**instance, **validated_data}

class TipoIngredienteSerializer(TipoReferenciaSerializer):
    class Meta:
        model = TipoIngrediente

class TipoUtensilioSerializer(TipoReferenciaSerializer):
    class Meta:
        model = TipoUtensilio

class PerfilSaborSerializer(TipoReferenciaSerializer):
    class Meta:
        model = PerfilSabor

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Unidade de Medida',
            value={
                'nome': 'ml',
                'nome_en': 'ml',
                'tipo': 'volume',
                'conversao_ml': 1.0
            }
        )
    ]
)
class UnidadeMedidaSerializer(serializers.Serializer):
    _id = ObjectIdField(required=False)
    nome = serializers.CharField(max_length=100)
    nome_en = serializers.CharField(max_length=100)
    tipo = serializers.ChoiceField(choices=['volume', 'peso', 'unidade'])
    conversao_ml = serializers.FloatField(required=False)

    def create(self, validated_data):
        result = UnidadeMedida.insert_one(validated_data)
        return UnidadeMedida.find_one({'_id': result.inserted_id})

    def update(self, instance, validated_data):
        UnidadeMedida.update_one(
            {'_id': instance['_id']},
            {'$set': validated_data}
        )
        return {**instance, **validated_data}

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Ingrediente',
            value={
                'nome': 'Rum Branco',
                'nome_en': 'White Rum',
                'tipo': 'destilado',
                'descricao': 'Rum claro, ideal para drinks',
                'unidades_permitidas': ['ml', 'oz']
            }
        )
    ]
)
class IngredienteSerializer(serializers.Serializer):
    _id = ObjectIdField(required=False)
    nome = serializers.CharField(max_length=100)
    nome_en = serializers.CharField(max_length=100)
    tipo = serializers.CharField(max_length=100)
    descricao = serializers.CharField(required=False, allow_blank=True)
    unidades_permitidas = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        result = Ingrediente.insert_one(validated_data)
        return Ingrediente.find_one({'_id': result.inserted_id})

    def update(self, instance, validated_data):
        Ingrediente.update_one(
            {'_id': instance['_id']},
            {'$set': validated_data}
        )
        return {**instance, **validated_data}

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Utensílio',
            value={
                'nome': 'Coqueteleira',
                'nome_en': 'Shaker',
                'tipo': 'preparo',
                'descricao': 'Utensílio para misturar drinks'
            }
        )
    ]
)
class UtensilioSerializer(serializers.Serializer):
    _id = ObjectIdField(required=False)
    nome = serializers.CharField(max_length=100)
    nome_en = serializers.CharField(max_length=100)
    tipo = serializers.CharField(max_length=100)
    descricao = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        result = Utensilio.insert_one(validated_data)
        return Utensilio.find_one({'_id': result.inserted_id})

    def update(self, instance, validated_data):
        Utensilio.update_one(
            {'_id': instance['_id']},
            {'$set': validated_data}
        )
        return {**instance, **validated_data}

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Drink',
            value={
                'nome': 'Mojito',
                'nome_en': 'Mojito',
                'nivel_dificuldade': 'facil',
                'teor_alcoolico': 'medio',
                'descricao': 'Drink cubano refrescante',
                'modo_preparo': '1. Amasse as folhas de hortelã...',
                'ingredientes': ['rum branco', 'hortelã', 'limão'],
                'utensilios': ['coqueteleira', 'pilão']
            }
        )
    ]
)
class DrinkSerializer(serializers.Serializer):
    _id = ObjectIdField(required=False)
    nome = serializers.CharField(max_length=100)
    nome_en = serializers.CharField(max_length=100)
    nivel_dificuldade = serializers.ChoiceField(choices=['facil', 'medio', 'dificil'])
    teor_alcoolico = serializers.ChoiceField(choices=['zero', 'baixo', 'medio', 'alto'])
    descricao = serializers.CharField(required=False, allow_blank=True)
    modo_preparo = serializers.CharField()
    ingredientes = serializers.ListField(child=serializers.CharField())
    utensilios = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        result = Drink.insert_one(validated_data)
        return Drink.find_one({'_id': result.inserted_id})

    def update(self, instance, validated_data):
        Drink.update_one(
            {'_id': instance['_id']},
            {'$set': validated_data}
        )
        return {**instance, **validated_data} 