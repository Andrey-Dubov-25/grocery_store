from rest_framework import serializers

from product.models import Category, Product, SubCategory, ProductImage


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий."""

    class Meta:
        model = SubCategory
        fields = ('name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'subcategories')


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'size_type')


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='subcategory.category.name')
    subcategory = serializers.CharField(source='subcategory.name')
    images = ProductImageSerializer(many=True, read_only=True)


    class Meta:
        model = Product
        fields = (
            'name', 'slug', 'category', 'subcategory', 'price', 'images'
        )
