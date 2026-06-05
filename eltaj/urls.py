"""URL configuration for eltaj project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Гриль-дом «от Элтаджа»'
admin.site.site_title = 'от Элтаджа'
admin.site.index_title = 'Управление магазином'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
