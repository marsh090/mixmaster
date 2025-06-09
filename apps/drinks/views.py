from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from bson import ObjectId
from .models import (
    TipoIngrediente, TipoUtensilio, UnidadeMedida,
    PerfilSabor, Ingrediente, Utensilio, Drink
)
from .serializers import (
    TipoIngredienteSerializer, TipoUtensilioSerializer, UnidadeMedidaSerializer,
    PerfilSaborSerializer, IngredienteSerializer, UtensilioSerializer, DrinkSerializer
)

@extend_schema_view(
    list=extend_schema(summary="Listar itens"),
    create=extend_schema(summary="Criar item"),
    retrieve=extend_schema(
        summary="Detalhes do item",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="ID do item (ObjectId)"
            )
        ]
    ),
    update=extend_schema(
        summary="Atualizar item",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="ID do item (ObjectId)"
            )
        ]
    ),
    destroy=extend_schema(
        summary="Remover item",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="ID do item (ObjectId)"
            )
        ]
    )
)
class MongoViewSet(viewsets.ViewSet):
    """ViewSet base para modelos MongoDB"""
    
    def get_object(self, pk):
        try:
            return self.model_class.find_one({'_id': ObjectId(pk)})
        except:
            return None

    def list(self, request):
        objects = list(self.model_class.find())
        serializer = self.serializer_class(objects, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def update(self, request, pk=None):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.model_class.delete_one({'_id': ObjectId(pk)})
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(summary="Listar tipos de ingrediente"),
    create=extend_schema(summary="Criar tipo de ingrediente"),
    retrieve=extend_schema(summary="Detalhes do tipo de ingrediente"),
    update=extend_schema(summary="Atualizar tipo de ingrediente"),
    destroy=extend_schema(summary="Remover tipo de ingrediente")
)
class TipoIngredienteViewSet(MongoViewSet):
    serializer_class = TipoIngredienteSerializer
    model_class = TipoIngrediente

@extend_schema_view(
    list=extend_schema(summary="Listar tipos de utensílio"),
    create=extend_schema(summary="Criar tipo de utensílio"),
    retrieve=extend_schema(summary="Detalhes do tipo de utensílio"),
    update=extend_schema(summary="Atualizar tipo de utensílio"),
    destroy=extend_schema(summary="Remover tipo de utensílio")
)
class TipoUtensilioViewSet(MongoViewSet):
    serializer_class = TipoUtensilioSerializer
    model_class = TipoUtensilio

@extend_schema_view(
    list=extend_schema(summary="Listar unidades de medida"),
    create=extend_schema(summary="Criar unidade de medida"),
    retrieve=extend_schema(summary="Detalhes da unidade de medida"),
    update=extend_schema(summary="Atualizar unidade de medida"),
    destroy=extend_schema(summary="Remover unidade de medida")
)
class UnidadeMedidaViewSet(MongoViewSet):
    serializer_class = UnidadeMedidaSerializer
    model_class = UnidadeMedida

@extend_schema_view(
    list=extend_schema(summary="Listar perfis de sabor"),
    create=extend_schema(summary="Criar perfil de sabor"),
    retrieve=extend_schema(summary="Detalhes do perfil de sabor"),
    update=extend_schema(summary="Atualizar perfil de sabor"),
    destroy=extend_schema(summary="Remover perfil de sabor")
)
class PerfilSaborViewSet(MongoViewSet):
    serializer_class = PerfilSaborSerializer
    model_class = PerfilSabor

@extend_schema_view(
    list=extend_schema(summary="Listar ingredientes"),
    create=extend_schema(summary="Criar ingrediente"),
    retrieve=extend_schema(summary="Detalhes do ingrediente"),
    update=extend_schema(summary="Atualizar ingrediente"),
    destroy=extend_schema(summary="Remover ingrediente")
)
class IngredienteViewSet(MongoViewSet):
    serializer_class = IngredienteSerializer
    model_class = Ingrediente

    @extend_schema(summary="Buscar ingredientes por texto")
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Busca ingredientes por texto no nome"""
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        # Busca case-insensitive no nome
        ingredientes = self.model_class.get_collection().find({
            "nome": {"$regex": query, "$options": "i"}
        }).limit(10)
        
        serializer = self.serializer_class(list(ingredientes), many=True)
        return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(summary="Listar utensílios"),
    create=extend_schema(summary="Criar utensílio"),
    retrieve=extend_schema(summary="Detalhes do utensílio"),
    update=extend_schema(summary="Atualizar utensílio"),
    destroy=extend_schema(summary="Remover utensílio")
)
class UtensilioViewSet(MongoViewSet):
    serializer_class = UtensilioSerializer
    model_class = Utensilio

    @extend_schema(summary="Buscar utensílios por texto")
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Busca utensílios por texto no nome"""
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        # Busca case-insensitive no nome
        utensilios = self.model_class.get_collection().find({
            "nome": {"$regex": query, "$options": "i"}
        }).limit(10)
        
        serializer = self.serializer_class(list(utensilios), many=True)
        return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(summary="Listar drinks"),
    create=extend_schema(summary="Criar drink"),
    retrieve=extend_schema(summary="Detalhes do drink"),
    update=extend_schema(summary="Atualizar drink"),
    destroy=extend_schema(summary="Remover drink"),
    search=extend_schema(
        summary="Buscar drinks por texto",
        parameters=[
            OpenApiParameter(
                name="q",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Texto para busca no nome ou descrição"
            )
        ]
    ),
    duplicate=extend_schema(
        summary="Duplicar drink existente",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="ID do drink a ser duplicado"
            )
        ]
    )
)
class DrinkViewSet(MongoViewSet):
    serializer_class = DrinkSerializer
    model_class = Drink

    def get_queryset(self):
        """Filtra drinks baseado em parâmetros"""
        queryset = self.model_class.get_collection().find()
        
        # Filtros
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categorias=categoria)
        
        dificuldade = self.request.query_params.get('dificuldade', None)
        if dificuldade:
            queryset = queryset.filter(nivel_dificuldade=dificuldade)
        
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Busca drinks por texto no nome ou descrição"""
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        # Busca case-insensitive no nome ou descrição
        drinks = self.model_class.get_collection().find({
            "$or": [
                {"nome": {"$regex": query, "$options": "i"}},
                {"descricao": {"$regex": query, "$options": "i"}}
            ]
        }).limit(10)
        
        serializer = self.serializer_class(list(drinks), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplica um drink existente"""
        drink = self.get_object(pk)
        if not drink:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Remove campos únicos e de controle
        drink.pop('_id', None)
        drink.pop('criado_em', None)
        drink.pop('atualizado_em', None)
        drink['nome'] = f"Cópia de {drink['nome']}"
        
        serializer = self.serializer_class(data=drink, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
