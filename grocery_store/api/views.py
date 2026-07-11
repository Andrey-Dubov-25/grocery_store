from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from product.models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Category.objects.prefetch_related('subcategories')


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Product.objects.select_related(
            'subcategory', 'subcategory__category'
        ).prefetch_related('images')