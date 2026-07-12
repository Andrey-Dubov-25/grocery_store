from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from djoser.views import UserViewSet
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    AddToCartView,
    CartClearView,
    CartItemDetailView,
    CartView,
    CategoryList,
    ProductList,
)


app_name = 'api'


schema_view = get_schema_view(
    openapi.Info(
        title='Grocery Store API',
        default_version='v1',
        description='Документация для проекта Grocery Store',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category'),
    path('products/', ProductList.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart-list'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/clear/', CartClearView.as_view(), name='cart-clear'),
    path(
        'cart/product/<int:id>/',
        CartItemDetailView.as_view(),
        name='cart-product-detail'
    ),
    path(
        'auth/register/',
        UserViewSet.as_view({'post': 'create'}),
        name='register',
    ),
    path(
        'auth/login/',
        TokenObtainPairView.as_view(),
        name='login',
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    )
]
