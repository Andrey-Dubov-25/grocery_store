import pytest

from django.test.client import Client
from rest_framework_simplejwt.tokens import AccessToken

from product.models import Cart, CartItem, Category, Product, SubCategory


@pytest.fixture
def author(django_user_model):
    """Фикстура автора корзины."""
    return django_user_model.objects.create_user(
        username='Автор', password='testpassword'
    )


@pytest.fixture
def author_client(author):
    """Фикстура авторизированного автора корзины."""
    client = Client()
    token = str(AccessToken.for_user(author))
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return client


@pytest.fixture
def cart(author):
    """Фикстура корзины."""
    return Cart.objects.create(user=author)


@pytest.fixture
def category_data():
    """Фикстура данных для создания категории."""
    return {
        'name': 'test_category',
        'slug': 'test'
    }


@pytest.fixture
def category(category_data):
    """Фикстура создания категории."""
    return Category.objects.create(**category_data)


@pytest.fixture
def subcategory_data(category):
    """Фикстура данных для создания подкатегории."""
    return {
        'name': 'test_subcategory',
        'slug': 'subtest',
        'category': category
    }


@pytest.fixture
def subcategory(subcategory_data):
    """Фикстура создания подкатегории."""
    return SubCategory.objects.create(**subcategory_data)


@pytest.fixture
def product_data(subcategory):
    """Фикстура данных для создания продукта."""
    return {
        'name': 'test_product',
        'slug': 'product_test',
        'price': 100.00,
        'subcategory': subcategory
    }


@pytest.fixture
def product(product_data):
    """Фикстура создания продукта."""
    return Product.objects.create(**product_data)


@pytest.fixture
def product_in_cart(product, cart):
    """Фикстура продукта в корзине."""
    return CartItem.objects.create(cart=cart, product=product)
