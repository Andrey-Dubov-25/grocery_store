from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from api import urls as api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)