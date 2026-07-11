from django.urls import path

from .views import (
    AddToCartView,
    CartClearView,
    CartItemDetailView,
    CartView,
    CategoryList,
    ProductList,
)


app_name = 'api'


urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category'),
    path('products/', ProductList.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/clear/', CartClearView.as_view(), name='cart-clear'),
    path(
        'cart/items/<int:item_id>/',
        CartItemDetailView.as_view(),
        name='cart-item-detail'
    ),
]
