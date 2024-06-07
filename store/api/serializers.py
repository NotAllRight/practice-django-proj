from rest_framework import serializers

from .models import Product, Order, Invoice


class ProductSerializer(serializers.ModelSerializer):
    """Клас серіалізаторів продуктів"""

    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_discount_price(self, obj):
        return obj.discount_price
    

class OrderSerializer(serializers.ModelSerializer):
    """Клас серіалізаторів замовлень"""

    price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    # Геттер цiни
    def get_price(self, obj):
        return obj.price
    
    # Гетер знижкової ціни
    def get_discount_price(self, obj):
        return obj.discount_price


class InvoiceSerializer(serializers.ModelSerializer):
    """Клас серіалізаторів рахункiв"""

    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    order_creation_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = "__all__"

    # Геттер назви продукту
    def get_product_name(self, obj):
        return obj.product_name
    
    # Геттер цiни продукту
    def get_product_price(self, obj):
        return obj.product_price
    # Геттер дати створення замовлення
    def get_order_creation_date(self, obj):
        return obj.order_creation_date