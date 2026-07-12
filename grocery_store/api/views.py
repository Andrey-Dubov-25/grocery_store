from decimal import Decimal

from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Cart, CartItem, Category, Product
from .serializers import (
    CartItemCreateSerializer,
    CartItemSerializer,
    CategorySerializer,
    ProductSerializer,
)


class CategoryList(generics.ListAPIView):
    """
    Возвращает список категорий с подкатегориям.

    - Доступно всем пользователям.
    - Доступна пагинация.
    """

    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Category.objects.prefetch_related('subcategories')


class ProductList(generics.ListAPIView):
    """
    Возвращает список продуктов.

    - Доступно всем пользователям.
    - Доступна пагинация.
    """

    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Возвращает queryset категорий с загруженными подкатегориями."""
        return Product.objects.select_related(
            'subcategory', 'subcategory__category'
        ).prefetch_related('images')


class AddToCartView(APIView):
    """Добавляет товар в корзину или увеличивает его количество."""

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data.get('product_id')
        quantity = serializer.validated_data.get('quantity')
        cart_item, is_created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id
        )

        if not is_created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=['quantity'])

        detail_serializer = CartItemSerializer(cart_item)
        status_code = (
            status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
        )
        return Response(detail_serializer.data, status=status_code)


class CartItemDetailView(APIView):
    """Редактирование наличия товара в корзине."""

    @staticmethod
    def get_product(user, id):
        """
        Возвращает товар из корзины, принадлежащей конкретному пользователю.
        """
        cart, _ = Cart.objects.get_or_create(user=user)
        return get_object_or_404(CartItem, id=id, cart=cart)

    def patch(self, request, id):
        """Обновление количества товара в корзине."""
        item = self.get_product(request.user, id)
        serializer = CartItemSerializer(
            instance=item,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        """Удаление товара из корзины."""
        item = self.get_product(request.user, id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):
    """Возвращает все товары из корзины."""

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart).select_related('product')
        total_items = 0
        total_amount = Decimal('0')
        serialized_items = []

        for item in items:
            quantity = item.quantity
            price = item.product.price
            total_items += quantity
            total_amount += quantity * price
            serialized_items.append(CartItemSerializer(item).data)

        return Response({
            'items': serialized_items,
            'total_items': total_items,
            'total_amount': total_amount,
        })


class CartClearView(APIView):
    """Полностью удаляет корзину пользователя."""
    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.filter(cart=cart).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
