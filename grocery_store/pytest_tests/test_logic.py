from http import HTTPStatus
from django.urls import reverse

from product.models import CartItem


def test_add_to_cart_product(author_client, product, cart):
    """Тестирование добавления продукта в корзину."""
    url = reverse('api:add-to-cart')
    data = {'product_id': product.id}
    response = author_client.post(url, data=data)

    assert response.status_code == HTTPStatus.CREATED


def test_add_to_cart_exist_product(
    author_client, product_in_cart, product, cart
):
    """Тестирование добавления существующего в корзине продукта."""
    url = reverse('api:add-to-cart')
    data_new = {'product_id': product.id, 'quantity': 5}
    response = author_client.post(url, data=data_new)

    assert response.status_code == HTTPStatus.OK

    cart_item = CartItem.objects.get(cart=cart, product=product)

    assert cart_item.quantity == 6


def test_delete_product_from_cart(
    author_client, product_in_cart, product, cart
):
    """Тестирование удаления продукта из корзины."""
    url = reverse('api:cart-product-detail', args=(product.id,))

    assert CartItem.objects.filter(cart=cart, product=product).count() == 1

    response = author_client.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert CartItem.objects.filter(cart=cart, product=product).count() == 0


def test_change_quantity_product_in_cart(author_client, product_in_cart):
    """Тестирование изменения количества товара в корзине."""
    url = reverse('api:cart-product-detail', args=(product_in_cart.id,))
    new_quantity = product_in_cart.quantity + 1
    data = {'quantity': new_quantity}
    response = author_client.patch(
        url,
        data=data,
        content_type='application/json'
    )

    assert response.status_code == HTTPStatus.OK

    updated_item = CartItem.objects.get(id=product_in_cart.id)

    assert updated_item.quantity == new_quantity


def test_delete_cart(author_client, product_in_cart, cart):
    """Тестирование очистки корзины."""
    url = reverse('api:cart-clear')

    assert CartItem.objects.filter(cart=cart).count() == 1

    response = author_client.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert CartItem.objects.filter(cart=cart).count() == 0
