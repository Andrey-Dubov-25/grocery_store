from django.core.validators import MinValueValidator
from rest_framework import serializers

from core import constants
from product.models import (
    CartItem,
    Category,
    Product,
    ProductImage,
    SubCategory,
)


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегории."""

    class Meta:
        model = SubCategory
        fields = ('name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'image', 'subcategories')


class ProductImageSerializer(serializers.ModelSerializer):
    """Сериализатор для фото продукта."""

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'size_type')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукта."""

    category = serializers.CharField(source='subcategory.category.name')
    subcategory = serializers.CharField(source='subcategory.name')
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'name', 'slug', 'category', 'subcategory', 'price', 'images'
        )


class CartItemCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления товара в корзину."""

    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(
        default=constants.MIN_QUANTITY,
        validators=[
            MinValueValidator(
                constants.MIN_QUANTITY,
                message=f'Количество должно быть не меньше {
                    constants.MIN_QUANTITY
                }'
            )
        ]
    )

    class Meta:
        model = CartItem
        fields = ('product_id', 'quantity')

    def validate_product_id(self, value):
        """Проверяет существование товара."""

        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                f'Продукт с ID {value} не существует'
            )

        return value


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор товара в корзине."""
    product = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(
        source='product.price',
        max_digits=constants.PRODUCT_PRICE_MAX_DIGITS,
        decimal_places=constants.PRODUCT_PRICE_DECIMAL_PLACES,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'price', 'quantity')
