from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import User
from .serializers import UserSerializer

class IsAdminOrSelf(permissions.BasePermission):
    """
    Permite que usuários admin acessem qualquer coisa,
    e usuários normais acessem apenas seus próprios dados
    """
    def has_object_permission(self, request, view, obj):
        # Admin pode fazer tudo
        if request.user.is_admin:
            return True
        # Usuário normal só pode acessar seus próprios dados
        return obj.id == request.user.id

@extend_schema_view(
    list=extend_schema(
        summary="Listar usuários",
        description="Retorna lista de usuários. Admins veem todos, usuários normais veem apenas a si mesmos.",
        responses={200: UserSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Criar usuário",
        description="Cria um novo usuário no sistema.",
        request=UserSerializer,
        responses={201: UserSerializer}
    ),
    retrieve=extend_schema(
        summary="Detalhes do usuário",
        description="Retorna detalhes de um usuário específico.",
        responses={200: UserSerializer}
    ),
    update=extend_schema(
        summary="Atualizar usuário",
        description="Atualiza todos os campos de um usuário.",
        request=UserSerializer,
        responses={200: UserSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar usuário parcialmente",
        description="Atualiza alguns campos de um usuário.",
        request=UserSerializer,
        responses={200: UserSerializer}
    ),
    destroy=extend_schema(
        summary="Remover usuário",
        description="Remove um usuário do sistema.",
        responses={204: None}
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        """
        Filtra queryset baseado no usuário:
        - Admin vê todos
        - Usuário normal vê apenas ele mesmo
        """
        if self.request.user.is_admin:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @extend_schema(
        summary="Criar novo usuário",
        description="Cria um novo usuário no sistema com os dados fornecidos.",
        responses={201: UserSerializer},
        examples=[
            OpenApiExample(
                'Exemplo de criação',
                value={
                    'email': 'novo@email.com',
                    'name': 'Novo Usuário',
                    'password': 'senha123'
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary="Atualizar usuário",
        description="Atualiza os dados de um usuário existente.",
        responses={200: UserSerializer},
        examples=[
            OpenApiExample(
                'Exemplo de atualização',
                value={
                    'name': 'Nome Atualizado',
                    'password': 'nova_senha'
                }
            )
        ]
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @extend_schema(
        summary="Remover usuário",
        description="Remove um usuário do sistema. Esta ação é irreversível.",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Perfil do usuário logado",
        description="Retorna os dados do usuário atualmente autenticado.",
        responses={200: UserSerializer}
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Retorna os dados do usuário logado
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

