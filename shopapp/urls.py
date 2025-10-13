from django.urls import path, include
from . import views
from .views import orders_export_view
from rest_framework.routers import DefaultRouter
from .api import ProductViewSet, OrderViewSet
from .feeds import LatestProductsFeed

app_name = 'shopapp'

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # Путь для главной страницы приложения в /shop/
    path('', views.ProductListView.as_view(), name='product_list'),

    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive/', views.ProductArchiveView.as_view(), name='product_archive'),

    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),

    path('upload/', views.upload_file_view, name='upload'),
    path('orders/export/', orders_export_view, name='orders_export'),

    path('products/latest/feed/', LatestProductsFeed(), name='products_feed'),

    # Автоматически добавленные маршруты REST API
    path('', include(router.urls)),
]