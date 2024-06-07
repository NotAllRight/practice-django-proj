from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import timedelta


class Product(models.Model):
    """Клас продуктiв"""

    name = models.CharField(max_length=200)
    price = models.FloatField(validators=[MinValueValidator(1)])
    creation_date = models.DateField(auto_now_add=True)

    # Знижкова ціна
    @property
    def discount_price(self):
        if timezone.now().date() - self.creation_date > timedelta(days=30):
            return round(self.price * 0.8, 2)
        return None

class Order(models.Model):
    """Клас замовлень"""

    product = models.OneToOneField("Product", on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=9,
        choices=[   # Валідні статуси замовлення
            ("NEW", "New"),
            ("PROCESSED", "Processed"),
            ("PAID", "Paid")
        ],
        default="NEW"
    )
    creation_date = models.DateField(auto_now_add=True)

    # Ціна продукту
    @property
    def price(self):
        return self.product.price

    # Знижкова ціна продукту
    @property
    def discount_price(self):
        return self.product.discount_price


class Invoice(models.Model):
    """Клас рахункiВ"""

    order = models.OneToOneField("Order", on_delete=models.DO_NOTHING)
    creation_date = models.DateField(auto_now_add=True)

    # Назва продукту
    @property
    def product_name(self):
        return self.order.product.name
    
    # Ціна продукту
    @property
    def product_price(self):
        return self.order.price
    
    # Дата створення замовлення
    @property
    def order_creation_date(self):
        return self.order.creation_date