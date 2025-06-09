from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# Rotas para coleções de referência
router.register(r'tipos-ingrediente', views.TipoIngredienteViewSet, basename='tipo-ingrediente')
router.register(r'tipos-utensilio', views.TipoUtensilioViewSet, basename='tipo-utensilio')
router.register(r'unidades-medida', views.UnidadeMedidaViewSet, basename='unidade-medida')
router.register(r'perfis-sabor', views.PerfilSaborViewSet, basename='perfil-sabor')

# Rotas para ingredientes e utensílios
router.register(r'ingredientes', views.IngredienteViewSet, basename='ingrediente')
router.register(r'utensilios', views.UtensilioViewSet, basename='utensilio')

# Rotas para drinks
router.register(r'drinks', views.DrinkViewSet, basename='drink')

urlpatterns = [
    path('', include(router.urls)),
] 