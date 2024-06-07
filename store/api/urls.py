from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import ProductViewSet, OrderViewSet, InvoiceViewSet
from users.views import CustomUserViewSet


router = DefaultRouter() # Базовий маршрутизатор
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'registration', CustomUserViewSet)

# Схема для відображення документації api
schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
)

urlpatterns = [
    # Шлях до документації api
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0)),
    path('', include(router.urls)),
]