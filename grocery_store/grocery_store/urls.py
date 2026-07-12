from django.contrib import admin
from django.urls import path, include
from api import urls as api


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include(api), name='api-root')
]
