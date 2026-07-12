# test_content.py
from django.urls import reverse


def test_product_in_cart(author_client, product_in_cart):
    """Тестирование содержания результирующего списка товаров."""
    url = reverse('api:cart-list')
    response = author_client.get(url)
    items = response.data.get('items')
    total_items = response.data.get('total_items')
    total_amount = response.data.get('total_amount')

    assert isinstance(items, list)
    assert total_items is not None
    assert total_amount is not None
    assert total_items == 1
