from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView

from core.views import UserViewSet, BarbeariaViewSet, ComodidadesViewSet, servicos_oferecidosViewSet,Horario_de_funcionamentoViewSet

from core.utils.virar_prop import VirarPropViewSet

router = DefaultRouter()

router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'virar-proprietario', VirarPropViewSet, basename='virar-prop')
router.register(r'barbearias', BarbeariaViewSet, basename='barbearias')
router.register(r'comodidades', ComodidadesViewSet, basename='comodidades')
router.register(r'servicos-oferecidos', servicos_oferecidosViewSet, basename='servicos-oferecidos')
router.register(r'horarios-funcionamento', Horario_de_funcionamentoViewSet, basename='horarios-funcionamento')

urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    # API
    path('api/', include(router.urls)),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path removido, agora o ViewSet está registrado no router
]
