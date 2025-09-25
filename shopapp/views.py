from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Product, Order
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import UploadFileForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from shopapp.models import Order
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, OrderSerializer



MAX_UPLOAD_SIZE = 1024 * 1024  # 1 Мб

def index(request):
    products = [
        {'name': 'Смартфон', 'price': 15000.565, 'created_at': datetime(2025, 1, 15)},
        {'name': 'Ноутбук', 'price': 55000, 'created_at': datetime(2025, 3, 10)},
        {'name': 'Часы', 'price': 7000.3, 'created_at': datetime(2025, 5, 5)},
    ]

    context = {
        'products': products,
        'current_date': datetime.now(),
    }
    return render(request, 'shopapp/index.html', context)


def shop_index(request):
    # Список основных ссылок (можно расширить)
    pages = [
        {'name': 'Products', 'url': 'products'},
        {'name': 'Orders', 'url': 'orders'}
    ]
    return render(request, 'shopapp/index.html', {'pages': pages})

def products_list(request):
    products = Product.objects.all()
    return render(request, 'shopapp/product_list.html', {'products': products})

def orders_list(request):
    # Для уменьшения количества запросов используем select_related и prefetch_related
    orders = Order.objects.select_related('user').prefetch_related('products').all()
    return render(request, 'shopapp/orders_list.html', {'orders': orders})


def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            if uploaded_file.size > MAX_UPLOAD_SIZE:
                return HttpResponseBadRequest("Ошибка: размер файла превышает 1 Мб.")

            # Здесь сохранение файла, например
            handle_uploaded_file(uploaded_file)

            return HttpResponse("Файл успешно загружен")
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    # Простое сохранение файла в папку media/uploads/ с оригинальным именем
    import os
    from django.conf import settings
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f.name)

    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class ProductListView(ListView):
    model = Product
    template_name = 'shopapp/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Показываем только неархивированные продукты
        return Product.objects.filter(is_archived=False)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopapp/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price']
    permission_required = 'shopapp.add_product'
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('shopapp:product_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price']
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('shopapp:product_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user.is_superuser or (user.has_perm('shopapp.change_product') and product.created_by == user)


class ProductArchiveView(View):
    template_name = 'shopapp/product_confirm_archive.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, self.template_name, {'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_archived = True
        product.save()
        return redirect('product_list')

# Orders views

class OrderListView(ListView):
    model = Order
    template_name = 'shopapp/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all().select_related('user').prefetch_related('products')


class OrderDetailView(DetailView):
    model = Order
    template_name = 'shopapp/order_detail.html'
    context_object_name = 'order'


class OrderCreateView(CreateView):
    model = Order
    fields = ['user', 'products']
    template_name = 'shopapp/order_form.html'
    success_url = reverse_lazy('order_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['user', 'products']
    template_name = 'shopapp/order_form.html'
    success_url = reverse_lazy('order_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'shopapp/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')


@user_passes_test(lambda u: u.is_staff)
def orders_export_view(request):
    orders = Order.objects.select_related('user').prefetch_related('products').all()

    orders_data = []
    for order in orders:
        orders_data.append({
            'id': order.id,
            'address': order.delivery_address,
            'promocode': order.promocode,
            'user_id': order.user.id,
            'product_ids': list(order.products.values_list('id', flat=True)),
        })

    return JsonResponse({'orders': orders_data})

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Поиск и сортировка
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']        # поля для поиска
    ordering_fields = ['price', 'name']            # поля для сортировки


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'ordered_at', 'created_at']
    ordering_fields = ['ordered_at', 'created_at', 'total_price']
