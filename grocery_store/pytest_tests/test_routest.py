import pytest
from http import HTTPStatus
from pytest_lazy_fixtures import lf

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('api:category', 'api:product')
)
def test_categories_products_availability_for_anonymous_user(client, name):
    """Тестирование доступности страниц категорий и продуктов анониму."""
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lf('client'), HTTPStatus.UNAUTHORIZED),
        (lf('author_client'), HTTPStatus.OK)
    )
)
def test_cart_availability_for_author(
    parametrized_client, expected_status, cart
):
    """
    Тестирование доступности корзины анониму и авторизированному пользователю.
    """
    url = reverse('api:cart-list')
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
