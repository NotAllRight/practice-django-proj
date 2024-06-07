import pytest


@pytest.fixture
def cashier(django_user_model):
    return django_user_model.objects.create(
        username='test_cashier', password=123, user_type='CASHIER'
    )

@pytest.fixture
def consultant(django_user_model):
    return django_user_model.objects.create(
        username='test_consultant', password=123, user_type='CONSULTANT'
    )

@pytest.fixture
def accountant(django_user_model):
    return django_user_model.objects.create(
        username='test_accountant', password=123, user_type='ACCOUNTANT'
    )
