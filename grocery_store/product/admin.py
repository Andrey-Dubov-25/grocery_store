from django.contrib import admin

from.models import Category, SubCategory, Product, Cart, CartItem, ProductImage


admin.site.empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Модель категории в админке.

    Настройки интерфейса:
    - list_display: вид в таблице списка пользователей;
    - list_filter: поля для фильтрации;
    - search_fields: поля для поиск;
    - ordering: поля для сортировки списка.

    Значения полей:
    * name - название категории;
    * slug - отображение в ссылке на сайте;
    """

    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name', 'slug',)
    ordering = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """
    Модель подкатегории в админке.

    Настройки интерфейса:
    - list_display: вид в таблице списка пользователей;
    - list_filter: поля для фильтрации;
    - search_fields: поля для поиск;
    - ordering: поля для сортировки списка.

    Значения полей:
    * name - название подкатегории;
    * slug - отображение в ссылке на сайте;
    """

    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name', 'slug',)
    ordering = ('name',)


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Модель продукта в админке.

    Настройки интерфейса:
    - list_display: вид в таблице списка пользователей;
    - list_filter: поля для фильтрации;
    - search_fields: поля для поиск;
    - ordering: поля для сортировки списка.

    Значения полей:
    * name - название продукта;
    * slug - отображение в ссылке на сайте;
    * price - цена продукта;
    * subcategory - подкатегория продукта.
    """

    list_display = ('name', 'slug', 'price', 'subcategory')
    list_filter = ('name',)
    search_fields = ('name', 'slug',)
    ordering = ('name',)
    inlines = (ProductImageInline, )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Модель продукта в админке.

    Настройки интерфейса:
    - list_display: вид в таблице списка пользователей;
    - list_filter: поля для фильтрации;
    - search_fields: поля для поиск;
    - ordering: поля для сортировки списка.

    Значения полей:
    * name - название продукта;
    * slug - отображение в ссылке на сайте;
    * price - цена продукта;
    * subcategory - подкатегория продукта.
    """

    list_display = ('user',)
    list_filter = ('user',)
    search_fields = ('user',)
    ordering = ('user',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Модель продукта в админке.

    Настройки интерфейса:
    - list_display: вид в таблице списка пользователей;
    - list_filter: поля для фильтрации;
    - search_fields: поля для поиск;
    - ordering: поля для сортировки списка.

    Значения полей:
    * name - название продукта;
    * slug - отображение в ссылке на сайте;
    * price - цена продукта;
    * subcategory - подкатегория продукта.
    """

    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart',)
    search_fields = ('cart',)
    ordering = ('cart',)
