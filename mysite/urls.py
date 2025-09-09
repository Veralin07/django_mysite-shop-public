"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from shopapp.views import upload_file_view  # если upload_file_view определён здесь
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny
from drf_spectacular.views import SpectacularRedocView
from django.contrib.sitemaps.views import sitemap
from shopapp.sitemaps import ShopSitemap


sitemaps = {
    'products': ShopSitemap,
}

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # для смены языка через URL

    path('admin/', admin.site.urls),

    # Редирект с корня '/' на '/shop/products/'
    path('', RedirectView.as_view(url='/shop/products/', permanent=False), name='index'),

    # Основное приложение с префиксом shop/
    path('shop/', include('shopapp.urls')),

    # Путь для загрузки файла
    path('upload/', upload_file_view, name='upload'),

    path('accounts/', include('myauth.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),

    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('shopapp/', include('shopapp.urls')),

    path('blog/', include('blogapp.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)