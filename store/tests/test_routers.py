import pytest
import itertools
from rest_framework.test import APIClient
from django.urls import reverse

from fixtures.fixture_users import cashier, consultant, accountant
from fixtures.fixture_data import *


"""-----------------------------GET tests-----------------------------"""
@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 200),
    ('consultant', 403),
    ('accountant', 403)
])
def test_product_list(user, status_code, request, product):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(reverse('product-list'))
    assert response.status_code == status_code

@pytest.mark.django_db
@pytest.mark.parametrize('user, order_status_list, status_code', [
    ('cashier', ['PROCESSED'], 200),
    ('consultant', ['NEW'], 200),
    ('accountant', ['NEW', 'PROCESSED', 'PAID'], 200)
])
def test_order_list(user, order_status_list, status_code, request):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(reverse('order-list'))
    assert response.status_code == status_code

    # Перевіряємо, що статус кожного замовлення у
    # відповіді входить в order_status_list
    for order in response.data:
        assert order['status'] in order_status_list

@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 403),
    ('consultant', 403),
    ('accountant', 403)
])
def test_invoice_list(user, status_code, request):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(reverse('invoice-list'))
    assert response.status_code == status_code

"""-----------------------------POST tests-----------------------------"""
@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 403),
    ('consultant', 403),
    ('accountant', 403)
])
def test_product_create(user, status_code, request):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        reverse('product-list'),
        {'name':'Test create product','price':'2555.99'}
    )
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 201),
    ('consultant', 403),
    ('accountant', 403)
])
def test_order_create(user, status_code, request, product):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        reverse('order-list'),
        {'product':product.id,'status':'NEW'}
    )
    assert response.status_code == status_code

@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 201),
    ('consultant', 403),
    ('accountant', 403)
])
def test_invoice_create(user, status_code, request, order):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(reverse('invoice-list'),{'order':order.id})
    assert response.status_code == status_code

"""-----------------------------PATCH tests-----------------------------"""
@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 403),
    ('consultant', 403),
    ('accountant', 403)
])
def test_product_update(user, status_code, request, product):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.patch(
        reverse('product-detail', kwargs={'pk':product.id}),
        {'name':'Changed name'}
    )
    assert response.status_code == status_code

@pytest.mark.django_db
@pytest.mark.parametrize('user, visible_statuses, allowed_transitions', [
    ('cashier', ['PROCESSED'], [('PROCESSED', 'PAID')]),
    ('consultant', ['NEW'], [('NEW', 'PROCESSED')]),
    ('accountant', ['NEW', 'PROCESSED', 'PAID'], [])
])
def test_order_update(user, visible_statuses, allowed_transitions, request, order):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)

    order_status_list = ['NEW', 'PROCESSED', 'PAID']
    for start_status, end_status in itertools.product(order_status_list, repeat=2):
        if start_status not in visible_statuses:
            continue  # пропускаємо статуси, які користувач не може бачити
        order.status = start_status
        order.save()
        response = client.patch(
            reverse('order-detail', kwargs={'pk':order.id}),
            {'status':end_status}
        )
        # Статус 200, якщо початковий і кінцевий статус замовлення 
        # відповідають дозволам, інакше - 403
        expected_status_code = 200 if (start_status, end_status) in allowed_transitions else 403
        assert response.status_code == expected_status_code

@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 403),
    ('consultant', 403),
    ('accountant', 403)
])
def test_invoice_update(user, status_code, request, invoice, order_2):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.patch(
        reverse('invoice-detail', kwargs={'pk':invoice.id}),
        {'order':order_2.id}
    )
    assert response.status_code == status_code

"""-----------------------------PUT tests-----------------------------"""
@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 403),
    ('consultant', 403),
    ('accountant', 403)
])
def test_product_change(user, status_code, request, product):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.put(
        reverse('product-detail', kwargs={'pk':product.id}),
        {'name':'New name', 'price':1.0}
    )
    assert response.status_code == status_code

@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code, order_fixture', [
    ('cashier', 403, 'order_3'),
    ('consultant', 403, 'order_2'),
    ('accountant', 403, 'order')
])
def test_order_change(user, status_code, order_fixture, request):
    user = request.getfixturevalue(user)
    order = request.getfixturevalue(order_fixture)
    client = APIClient()
    client.force_authenticate(user=user)
    new_product = Product.objects.create(name='New product', price=333.33)
    response = client.put(
        reverse('order-detail', kwargs={'pk':order.id}),
        {'status':'NEW', 'product':new_product.id}
    )
    assert response.status_code == status_code

@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 403),
    ('consultant', 403),
    ('accountant', 403)
])
def test_invoice_change(user, status_code, request, invoice, order_2):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.put(
        reverse('invoice-detail', kwargs={'pk':invoice.id}),
        {'order':order_2.id}
    )
    assert response.status_code == status_code

"""-----------------------------DELETE tests-----------------------------"""
@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 403),
    ('consultant', 403),
    ('accountant', 403)
])
def test_product_delete(user, status_code, request, product):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete(
        reverse('product-detail', kwargs={'pk':product.id}))
    assert response.status_code == status_code

@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code, order_fixture', [
    ('cashier', 403, 'order_3'),
    ('consultant', 403, 'order_2'),
    ('accountant', 403, 'order')
])
def test_order_delete(user, status_code, order_fixture, request):
    user = request.getfixturevalue(user)
    order = request.getfixturevalue(order_fixture)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete(
        reverse('order-detail', kwargs={'pk':order.id}))
    assert response.status_code == status_code

@pytest.mark.django_db
@pytest.mark.parametrize('user, status_code', [
    ('cashier', 403),
    ('consultant', 403),
    ('accountant', 403)
])
def test_invoice_delete(user, status_code, request, invoice):
    user = request.getfixturevalue(user)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete(
        reverse('invoice-detail', kwargs={'pk':invoice.id}))
    assert response.status_code == status_code