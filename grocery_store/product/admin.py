from django.contrib import admin

from .models import Category, SubCategory, Product, ProductImage


admin.site.empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Модель категории в админке."""

    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name', 'slug',)
    ordering = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Модель подкатегории в админке."""

    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name', 'slug',)
    ordering = ('name',)


class ProductImageInline(admin.StackedInline):
    """Модель фото продукта в админке."""
    model = ProductImage
    max_num = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Модель продукта в админке."""

    list_display = ('name', 'slug', 'price', 'subcategory')
    list_filter = ('name',)
    search_fields = ('name', 'slug',)
    ordering = ('name',)
    inlines = (ProductImageInline, )
