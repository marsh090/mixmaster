from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from apps.drinks.admin import admin_site

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'message': 'MixMaster API is running'
    })

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),

    # Admin
    path('admin/', admin_site.urls),

    # API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Apps
    path('api/drinks/', include('apps.drinks.urls')),
]
