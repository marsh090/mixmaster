from rest_framework import serializers
from bson import ObjectId
from .models import (
    TipoIngrediente, TipoUtensilio, UnidadeMedida,
    PerfilSabor, Ingrediente, Utensilio, Drink
)

class ObjectIdField(serializers.Field):
    """Campo personalizado para serializar/deserializar ObjectId do MongoDB"""
    
    def to_representation(self, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    def to_internal_value(self, data):
        try:
            return ObjectId(str(data))
        except Exception:
            raise serializers.ValidationError('ID inválido')

class TipoIngredienteSerializer(serializers.Serializer):
    id = ObjectIdField(source='_id', read_only=True)
    nome = serializers.CharField(max_length=100)
    nome_en = serializers.CharField(max_length=100)
    ordem = serializers.IntegerField()

    def create(self, validated_data):
        return TipoIngrediente.create(validated_data)

    def update(self, instance, validated_data):
        TipoIngrediente.update(instance['_id'], validated_data)
        return {**instance, **validated_data}

class TipoUtensilioSerializer(serializers.Serializer):
    id = ObjectIdField(source='_id', read_only=True)
    nome = serializers.CharField(max_length=100)
    nome_en = serializers.CharField(max_length=100)
    ordem = serializers.IntegerField()

    def create(self, validated_data):
        return TipoUtensilio.create(validated_data)

    def update(self, instance, validated_data):
        TipoUtensilio.update(instance['_id'], validated_data)
        return {**instance, **validated_data}

class UnidadeMedidaSerializer(serializers.Serializer):
    id = ObjectIdField(source='_id', read_only=True)
    nome = serializers.CharField(max_length=50)
    nome_en = serializers.CharField(max_length=50)
    tipo = serializers.CharField(max_length=50)
    conversao_ml = serializers.FloatField(allow_null=True)

    def create(self, validated_data):
        return UnidadeMedida.create(validated_data)

    def update(self, instance, validated_data):
        UnidadeMedida.update(instance['_id'], validated_data)
        return {**instance, **validated_data}

class PerfilSaborSerializer(serializers.Serializer):
    id = ObjectIdField(source='_id', read_only=True)
    nome = serializers.CharField(max_length=50)
    nome_en = serializers.CharField(max_length=50)
    ordem = serializers.IntegerField()

    def create(self, validated_data):
        return PerfilSabor.create(validated_data)

    def update(self, instance, validated_data):
        PerfilSabor.update(instance['_id'], validated_data)
        return {**instance, **validated_data}

class IngredienteSerializer(serializers.Serializer):
    id = ObjectIdField(source='_id', read_only=True)
    nome = serializers.CharField(max_length=100)
    nome_en = serializers.CharField(max_length=100)
    tipo = serializers.CharField(max_length=100)
    unidades_permitidas = serializers.ListField(
        child=serializers.CharField(max_length=50)
    )
    descricao = serializers.CharField(max_length=500, allow_blank=True)

    def validate_tipo(self, value):
        """Validar se o tipo de ingrediente existe"""
        tipo = TipoIngrediente.find_one({"nome": value})
        if not tipo:
            raise serializers.ValidationError(f"Tipo de ingrediente '{value}' não existe")
        return value

    def validate_unidades_permitidas(self, value):
        """Validar se todas as unidades existem"""
        for unidade in value:
            if not UnidadeMedida.find_one({"nome": unidade}):
                raise serializers.ValidationError(f"Unidade '{unidade}' não existe")
        return value

    def create(self, validated_data):
        return Ingrediente.create(validated_data)

    def update(self, instance, validated_data):
        Ingrediente.update(instance['_id'], validated_data)
        return {**instance, **validated_data}

class UtensilioSerializer(serializers.Serializer):
    id = ObjectIdField(source='_id', read_only=True)
    nome = serializers.CharField(max_length=100)
    nome_en = serializers.CharField(max_length=100)
    tipo = serializers.CharField(max_length=100)
    descricao = serializers.CharField(max_length=500, allow_blank=True)

    def validate_tipo(self, value):
        """Validar se o tipo de utensílio existe"""
        tipo = TipoUtensilio.find_one({"nome": value})
        if not tipo:
            raise serializers.ValidationError(f"Tipo de utensílio '{value}' não existe")
        return value

    def create(self, validated_data):
        return Utensilio.create(validated_data)

    def update(self, instance, validated_data):
        Utensilio.update(instance['_id'], validated_data)
        return {**instance, **validated_data}

class IngredienteDrinkSerializer(serializers.Serializer):
    """Serializer para ingredientes dentro de um drink"""
    ingrediente_id = ObjectIdField()
    quantidade = serializers.FloatField(min_value=0)
    unidade = serializers.CharField(max_length=50)
    opcional = serializers.BooleanField(default=False)
    ordem = serializers.IntegerField()

    def validate(self, data):
        """Validar se ingrediente existe e se unidade é permitida"""
        ingrediente = Ingrediente.find_one({"_id": data['ingrediente_id']})
        if not ingrediente:
            raise serializers.ValidationError("Ingrediente não existe")
        
        if data['unidade'] not in ingrediente['unidades_permitidas']:
            raise serializers.ValidationError(
                f"Unidade '{data['unidade']}' não é permitida para este ingrediente"
            )
        return data

class PassoPreparoSerializer(serializers.Serializer):
    """Serializer para passos de preparo de um drink"""
    ordem = serializers.IntegerField()
    descricao = serializers.CharField(max_length=500)
    dica = serializers.CharField(max_length=500, allow_blank=True, required=False)
    utensilios = serializers.ListField(
        child=ObjectIdField(),
        required=False
    )

    def validate_utensilios(self, value):
        """Validar se todos os utensílios existem"""
        for utensilio_id in value:
            if not Utensilio.find_one({"_id": utensilio_id}):
                raise serializers.ValidationError(f"Utensílio '{utensilio_id}' não existe")
        return value

class DrinkSerializer(serializers.Serializer):
    id = ObjectIdField(source='_id', read_only=True)
    nome = serializers.CharField(max_length=100)
    nome_en = serializers.CharField(max_length=100)
    slug = serializers.CharField(max_length=100, read_only=True)
    descricao = serializers.CharField(max_length=500)
    imagem_url = serializers.URLField(allow_blank=True, required=False)
    criado_em = serializers.DateTimeField(read_only=True)
    atualizado_em = serializers.DateTimeField(read_only=True)
    criado_por = ObjectIdField(read_only=True)
    
    categorias = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False
    )
    nivel_dificuldade = serializers.ChoiceField(
        choices=['fácil', 'médio', 'difícil'],
        required=False
    )
    tempo_preparo = serializers.IntegerField(min_value=1, required=False)
    teor_alcoolico = serializers.ChoiceField(
        choices=['zero', 'baixo', 'médio', 'alto'],
        required=False
    )
    
    ingredientes = IngredienteDrinkSerializer(many=True)
    
    preparo = serializers.DictField(
        child=serializers.Field(),
        required=True
    )
    
    perfil_sabor = serializers.DictField(
        child=serializers.IntegerField(min_value=0, max_value=5),
        required=False
    )
    
    ocasioes = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False
    )
    
    harmonizacao = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False
    )
    
    clima = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False
    )

    def create(self, validated_data):
        from django.utils.text import slugify
        from datetime import datetime
        
        # Gerar slug
        validated_data['slug'] = slugify(validated_data['nome'])
        
        # Adicionar timestamps
        validated_data['criado_em'] = datetime.utcnow()
        validated_data['atualizado_em'] = datetime.utcnow()
        
        # Adicionar usuário que criou (deve vir do contexto)
        if self.context and 'request' in self.context:
            validated_data['criado_por'] = self.context['request'].user.id
        
        return Drink.create(validated_data)

    def update(self, instance, validated_data):
        from datetime import datetime
        
        # Atualizar timestamp
        validated_data['atualizado_em'] = datetime.utcnow()
        
        Drink.update(instance['_id'], validated_data)
        return {**instance, **validated_data} 