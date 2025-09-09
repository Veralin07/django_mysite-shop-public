from django.urls import path
from . import views
from .views import orders_export_view, UserOrdersListView, UserOrdersExportView
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api import ProductViewSet, OrderViewSet
from .feeds import LatestProductsFeed


app_name = 'shopapp'

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # path('', index, name='index'),
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
    path('', include(router.urls)),

    path('products/latest/feed/', LatestProductsFeed(), name='products_feed'),

    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_orders_list'),
    path('users/<int:user_id>/orders/export/', UserOrdersExportView.as_view(), name='user_orders_export'),
]