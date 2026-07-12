from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from core import constants

User = get_user_model()


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(
        max_length=constants.CATEGORY_NAME_LEN,
        verbose_name='Название',
        help_text='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=constants.CATEGORY_SLUG_LEN,
        verbose_name='Слаг',
        help_text='Отображение в ссылке на сайте'
    )
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Изображение категории',
        upload_to='categories/'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Возвращает строковое представление."""
        return self.name


class SubCategory(models.Model):
    """Модель подкатегорий."""
    name = models.CharField(
        max_length=constants.SUBCATEGORY_NAME_LEN,
        verbose_name='Название',
        help_text='Название подкатегории'
    )

    slug = models.SlugField(
        unique=True,
        max_length=constants.SUBCATEGORY_SLUG_LEN,
        verbose_name='Слаг',
        help_text='Отображение в ссылке на сайте'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        help_text='Родительская категория',
        related_name='subcategories'
    )
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Изображение подкатегории',
        upload_to='subcategories/'
    )

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        """Возвращает строковое представлении."""
        return self.name


class Product(models.Model):
    """Модель продуктов."""
    name = models.CharField(
        max_length=constants.PRODUCT_NAME_LEN,
        verbose_name='Продукт',
        help_text='Название продукта'
    )
    slug = models.SlugField(
        unique=True,
        max_length=constants.PRODUCT_SLUG_LEN,
        verbose_name='Слаг',
        help_text='Отображение в ссылке на сайте'
    )
    price = models.DecimalField(
        max_digits=constants.PRODUCT_PRICE_MAX_DIGITS,
        decimal_places=constants.PRODUCT_PRICE_DECIMAL_PLACES,
        verbose_name='Цена',
        help_text='Цена товара'
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        verbose_name='Подкатегория',
        help_text='Подкатегория товара',
        related_name='products'
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        """Возвращает строковое представление."""
        return self.name


class ProductImage(models.Model):
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Продукт'
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Файл изображения'
    )
    size_type = models.CharField(
        max_length=constants.MAX_SIZE_TYPE_LEN,
        choices=SIZE_CHOICES,
        verbose_name='Размер'
    )

    class Meta:
        verbose_name = 'изображение продукта'
        verbose_name_plural = 'Изображения продуктов'
        constraints = [
            models.UniqueConstraint(
                fields=('product', 'size_type'),
                name='unique_product_size_type'
            )
        ]

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
        help_text='Корзина пользователя'
    )

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина',
        help_text='Корзина пользователя'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Товар',
        help_text='Товар в корзине'
    )
    quantity = models.PositiveIntegerField(
        default=constants.MIN_QUANTITY,
        validators=[MinValueValidator(constants.MIN_QUANTITY)],
        verbose_name='Количество',
        help_text='Количество товара в корзине'
    )

    class Meta:
        verbose_name = 'элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        constraints = [
            models.UniqueConstraint(
                fields=('cart', 'product'),
                name='unique_cart_product'
            )
        ]

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'
