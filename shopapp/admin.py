from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Order, Product

class ProductInline(admin.TabularInline):
    extra = 0
    verbose_name = "Товар"
    verbose_name_plural = "Товары"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'ordered_at')
    search_fields = ('status', 'user__username')
    change_list_template = "admin/shopapp/orders_changelist.html"
    inlines = [ProductInline]

    def import_csv(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                # обработка файла (CSV/JSON/XML), создание заказов и привязка товаров
                # пример для CSV
                import csv, io

                data_set = file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                reader = csv.DictReader(io_string)
                for row in reader:
                    order = Order.objects.create(
                        status=row['status'],
                        user_id=row['user_id'],
                        notes=row.get('notes', '')
                    )
                    product_ids = row['product_ids'].split(',')
                    products = Product.objects.filter(id__in=product_ids)
                    order.products.set(products)
                    order.save()
                return redirect('admin:shopapp_order_changelist')
        else:
            form = UploadFileForm()
        return render(request, 'admin/csv_form.html', {'form': form})

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='shopapp_order_import_csv'),
        ]
        return custom_urls + urls

admin.site.register(Order)
admin.site.register(Product)  # Product можно регистрировать отдельно, без inlines
