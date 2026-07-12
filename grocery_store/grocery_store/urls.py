from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from djoser.views import UserViewSet
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from api import urls as api


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
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include(api), name='api-root'),
    path(
        'auth/register/',
        UserViewSet.as_view({'post': 'create'}),
        name='register',
    ),
    path(
        'auth/login/',
        TokenObtainPairView.as_view(),
        name='login',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
   path(
       'swagger<format>/',
       schema_view.without_ui(cache_timeout=0),
       name='schema-json'
    ),
   path(
       'swagger/',
       schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'
    ),
   path(
       'redoc/',
       schema_view.with_ui('redoc', cache_timeout=0),
       name='schema-redoc'
    ),
]
