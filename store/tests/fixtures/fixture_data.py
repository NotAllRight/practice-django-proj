import pytest

from api.models import Product, Order, Invoice


@pytest.fixture
def product():
    return Product.objects.create(name='Test product', price=100.0)

@pytest.fixture
def product_2():
    return Product.objects.create(name='Test product 2', price=200.0)

@pytest.fixture
def product_3():
    return Product.objects.create(name='Test product 3', price=300.0)

@pytest.fixture
def order(product):
    return Order.objects.create(product=product, status='PAID')

@pytest.fixture
def order_2(product_2):
    return Order.objects.create(product=product_2, status='NEW')

@pytest.fixture
def order_3(product_3):
    return Order.objects.create(product=product_3, status='PROCESSED')

@pytest.fixture
def invoice(order):
    return Invoice.objects.create(order=order)
