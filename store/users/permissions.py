from rest_framework import permissions, exceptions

from api.models import Order


class ProductViewPermissions(permissions.BasePermission):
    """Клас дозволів відображення продуктів"""

    def has_permission(self, request, view):
        return request.user.is_cashier or request.user.is_superuser
    

class ProductChangePermissions(permissions.BasePermission):
    """Клас дозволів зміни продуктів"""

    def has_permission(self, request, view):
        return request.user.is_superuser
    

class ProductCreatePermissions(permissions.BasePermission):
    """Клас дозволів створення продуктів"""

    def has_permission(self, request, view):
        return request.user.is_superuser


class ProductDeletePermissions(permissions.BasePermission):
    """Клас дозволів видалення продуктів"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class OrderViewPermissions(permissions.BasePermission):
    """Клас дозволів відображення замовлень"""

    def has_permission(self, request, view):
        return (request.user.is_cashier or
                request.user.is_consultant or
                request.user.is_accountant or
                request.user.is_superuser)


class OrderChangePermissions(permissions.BasePermission):
    """Клас дозволів зміни замовлень"""

    def has_object_permission(self, request, view, obj):
        # Заборона змiни iнших полiв, окрiм статусу
        if set(request.data.keys()) != {'status'} and not request.user.is_superuser:
            return False
        return (
        (request.user.is_consultant and obj.status == 'NEW' and request.data.get('status') == 'PROCESSED') or
        (request.user.is_cashier and obj.status == 'PROCESSED' and request.data.get('status') == 'PAID') or 
        request.user.is_superuser
        )


class OrderCreatePermissions(permissions.BasePermission):
    """Клас дозволів створення замовлень"""

    def has_permission(self, request, view):
        return ((request.user.is_cashier and request.data.get('status') == 'NEW') or
                request.user.is_superuser)


class OrderDeletePermissions(permissions.BasePermission):
    """Клас дозволів видалення замовлень"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class InvoiceViewPermissions(permissions.BasePermission):
    """Клас дозволів відображення рахункiв"""

    def has_permission(self, request, view):
        return request.user.is_superuser


class InvoiceChangePermissions(permissions.BasePermission):
    """Клас дозволів змiни рахункiв"""

    def has_permission(self, request, view):
        return request.user.is_superuser
    

class InvoiceCreatePermissions(permissions.BasePermission):
    """Клас дозволів створення рахункiв"""

    def has_permission(self, request, view):
        order_id = request.data.get('order')
        if order_id is not None:
            order = Order.objects.get(id=order_id)
            # Створення рахункiв можливо тiльки для замовлень зi статусом 'PAID'
            if order.status != 'PAID' and not request.user.is_superuser:
                raise exceptions.PermissionDenied("You can only create an invoice for an order with status 'PAID'")
        return request.user.is_cashier or request.user.is_superuser
    

class InvoiceDeletePermissions(permissions.BasePermission):
    """Клас дозволів видалення рахункiв"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
    