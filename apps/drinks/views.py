from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import (
    TipoIngrediente, TipoUtensilio, UnidadeMedida,
    PerfilSabor, Ingrediente, Utensilio, Drink
)
from .serializers import (
    TipoIngredienteSerializer, TipoUtensilioSerializer, UnidadeMedidaSerializer,
    PerfilSaborSerializer, IngredienteSerializer, UtensilioSerializer, DrinkSerializer
)

class BaseViewSet(viewsets.ViewSet):
    """ViewSet base com operações comuns"""
    permission_classes = [permissions.IsAuthenticated]
    model_class = None
    serializer_class = None

    def get_object(self, pk):
        from bson.objectid import ObjectId
        obj = self.model_class.find_one({"_id": ObjectId(pk)})
        if not obj:
            return None
        return obj

    def list(self, request):
        objects = self.model_class.find_all()
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
        self.model_class.delete(obj['_id'])
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(summary="Listar tipos de ingrediente"),
    create=extend_schema(summary="Criar tipo de ingrediente"),
    retrieve=extend_schema(summary="Detalhes do tipo de ingrediente"),
    update=extend_schema(summary="Atualizar tipo de ingrediente"),
    destroy=extend_schema(summary="Remover tipo de ingrediente"),
)
class TipoIngredienteViewSet(BaseViewSet):
    model_class = TipoIngrediente
    serializer_class = TipoIngredienteSerializer

@extend_schema_view(
    list=extend_schema(summary="Listar tipos de utensílio"),
    create=extend_schema(summary="Criar tipo de utensílio"),
    retrieve=extend_schema(summary="Detalhes do tipo de utensílio"),
    update=extend_schema(summary="Atualizar tipo de utensílio"),
    destroy=extend_schema(summary="Remover tipo de utensílio"),
)
class TipoUtensilioViewSet(BaseViewSet):
    model_class = TipoUtensilio
    serializer_class = TipoUtensilioSerializer

@extend_schema_view(
    list=extend_schema(summary="Listar unidades de medida"),
    create=extend_schema(summary="Criar unidade de medida"),
    retrieve=extend_schema(summary="Detalhes da unidade de medida"),
    update=extend_schema(summary="Atualizar unidade de medida"),
    destroy=extend_schema(summary="Remover unidade de medida"),
)
class UnidadeMedidaViewSet(BaseViewSet):
    model_class = UnidadeMedida
    serializer_class = UnidadeMedidaSerializer

@extend_schema_view(
    list=extend_schema(summary="Listar perfis de sabor"),
    create=extend_schema(summary="Criar perfil de sabor"),
    retrieve=extend_schema(summary="Detalhes do perfil de sabor"),
    update=extend_schema(summary="Atualizar perfil de sabor"),
    destroy=extend_schema(summary="Remover perfil de sabor"),
)
class PerfilSaborViewSet(BaseViewSet):
    model_class = PerfilSabor
    serializer_class = PerfilSaborSerializer

@extend_schema_view(
    list=extend_schema(summary="Listar ingredientes"),
    create=extend_schema(summary="Criar ingrediente"),
    retrieve=extend_schema(summary="Detalhes do ingrediente"),
    update=extend_schema(summary="Atualizar ingrediente"),
    destroy=extend_schema(summary="Remover ingrediente"),
)
class IngredienteViewSet(BaseViewSet):
    model_class = Ingrediente
    serializer_class = IngredienteSerializer

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
    destroy=extend_schema(summary="Remover utensílio"),
)
class UtensilioViewSet(BaseViewSet):
    model_class = Utensilio
    serializer_class = UtensilioSerializer

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
)
class DrinkViewSet(BaseViewSet):
    model_class = Drink
    serializer_class = DrinkSerializer

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

    @extend_schema(summary="Buscar drinks por texto")
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

    @extend_schema(summary="Duplicar drink existente")
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
