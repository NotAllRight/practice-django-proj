import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from fixtures.fixture_users import *
from fixtures.fixture_data import *


# Перевірка правильності підрахунку знижкової ціни
@pytest.mark.django_db
def test_discount_price():
    start_price = 100.0
    
    product_with_discount = Product.objects.create(
        name='Product with discount',
        price=start_price
    )
    product_with_discount.creation_date = timezone.now().date() - datetime.timedelta(days=33)
    product_with_discount.save()
    assert product_with_discount.discount_price == (start_price * 0.8)

    product_without_discount = Product.objects.create(
        name='Product without discount',
        price=start_price,
    )
    assert product_without_discount.discount_price is None

"""-----------------------------VALIDATION TESTS-----------------------------"""
@pytest.mark.django_db
def test_product_price_validation():
    # Спроба створити продукт з негативною ціною повинна викликати помилку валідації
    with pytest.raises(ValidationError):
        product = Product.objects.create(name='Invalid product', price=-100.0)
        product.full_clean()

    # Спроба створити продукт з нульовою ціною повинна викликати помилку валідації
    with pytest.raises(ValidationError):
        product = Product.objects.create(name='Invalid product', price=0.0)
        product.full_clean()

    # Спроба створити продукт з позитивною ціною повинна бути успішною
    product = Product.objects.create(name='Valid product', price=100.0)
    product.full_clean()

@pytest.mark.django_db
def test_order_status_validation(product, product_2):
    # Спроба створити продукт з некоректним статусом повинна
    # викликати помилку валідації
    with pytest.raises(ValidationError):
        order = Order.objects.create(product=product, status='INVALID STATUS')
        order.full_clean()

    # Спроба створити продукт з коректним статусом повинна бути успішною
    order = Order.objects.create(product=product_2, status='NEW')
    order.full_clean()

"""-----------------------------UNIQUE TESTS-----------------------------"""
@pytest.mark.django_db
def test_order_product_uniqueness(product):
    # Створюємо перше замовлення з продуктом
    Order.objects.create(product=product, status='NEW')

    # Спроба створити друге замовлення з тим самим продуктом 
    # повинна спричинити помилку унiкальностi
    with pytest.raises(IntegrityError):
        Order.objects.create(product=product, status='NEW')

@pytest.mark.django_db
def test_invoice_order_uniqueness(order):
    # Створюємо перший рахунок із замовленням
    Invoice.objects.create(order=order)

    # Спроба створити другий рахунок-фактуру з тим самим 
    # замовленням повинна спричинити помилку унiкальностi
    with pytest.raises(IntegrityError):
        Invoice.objects.create(order=order)