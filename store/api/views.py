from rest_framework import viewsets, exceptions
from django.utils.dateparse import parse_date

from .models import Product, Order, Invoice
from .serializers import ProductSerializer, OrderSerializer, InvoiceSerializer
from users.permissions import *


class ProductViewSet(viewsets.ModelViewSet):
    """Клас відображення до моделі Product"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Геттер дозволів
    def get_permissions(self):
        # Дозволи для створення об'єктів
        if self.action == 'create':
            permission_classes = [ProductCreatePermissions]
        # Дозволи для оновлення об'єктів
        elif self.action in ['update', 'partial_update']:
            permission_classes = [ProductChangePermissions]
        # Дозволи для видалення об'єктів
        elif self.action == 'destroy':
            permission_classes = [ProductDeletePermissions]
        # Дозволи для відображення  об'єктів
        else: 
            permission_classes = [ProductViewPermissions]
        return [permission() for permission in permission_classes]


class OrderViewSet(viewsets.ModelViewSet):
    """Клас відображення до моделі Order"""

    queryset = Order.objects.none()  # Значення за замовчуванням
    serializer_class = OrderSerializer

    # Геттер списку об'єктів таблиці
    def get_queryset(self):
        # Фільтрація замовлень за датою
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if self.request.user.is_accountant or self.request.user.is_superuser:
            # Якщо початкова і кінцева дата передані в маршруті, 
            # то повернути відфільтрований за датою список об'єктів
            if start_date is not None and end_date is not None:
                start_date = parse_date(start_date)
                end_date = parse_date(end_date)
                return Order.objects.filter(creation_date__range=(start_date, end_date))
            
        if self.request.user.is_consultant:
            # Заборона фільтрації за датою
            if start_date is not None or end_date is not None:
                raise exceptions.PermissionDenied()
            # Консультант може бачити тільки замовлення зі статусом'NEW'
            return Order.objects.filter(status='NEW')
        elif self.request.user.is_cashier:
            # Заборона фільтрації за датою
            if start_date is not None or end_date is not None:
                raise exceptions.PermissionDenied()
            # Касир може бачити тільки замовлення зі статусом'PROCESSED'
            return Order.objects.filter(status='PROCESSED')
            
        return Order.objects.all()

    # Геттер дозволів
    def get_permissions(self):
        # Дозволи для створення об'єктів
        if self.action == 'create':
            permission_classes = [OrderCreatePermissions]
        # Дозволи для оновлення об'єктів
        elif self.action in ['update', 'partial_update']:
            permission_classes = [OrderChangePermissions]
        # Дозволи для видалення об'єктів
        elif self.action == 'destroy':
            permission_classes = [OrderDeletePermissions]
        # Дозволи для відображення  об'єктів
        else:
            permission_classes = [OrderViewPermissions]
        return [permission() for permission in permission_classes]


class InvoiceViewSet(viewsets.ModelViewSet):
    """Клас відображення до моделі Invoice"""

    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    # Геттер дозволів
    def get_permissions(self):
        # Дозволи для створення об'єктів
        if self.action == 'create':
            permission_classes = [InvoiceCreatePermissions]
        # Дозволи для оновлення об'єктів
        elif self.action in ['update', 'partial_update']: 
            permission_classes = [InvoiceChangePermissions]
        # Дозволи для видалення об'єктів
        elif self.action == 'destroy':
            permission_classes = [InvoiceDeletePermissions]
        # Дозволи для відображення  об'єктів
        else: 
            permission_classes = [InvoiceViewPermissions] 
        return [permission() for permission in permission_classes]
