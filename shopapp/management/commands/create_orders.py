from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product
import random

class Command(BaseCommand):
    help = "Create sample orders linked to products"

    def handle(self, *args, **kwargs):
        # Получаем первого пользователя (предполагается, что создан superuser)
        user = User.objects.first()
        if not user:
            self.stdout.write("No users found. Create a superuser first.")
            return

        products = list(Product.objects.all())
        if not products:
            self.stdout.write("No products found. Run create_products first.")
            return

        orders_data = [
            {'notes': 'First order', 'status': 'new'},
            {'notes': 'Second order', 'status': 'pending'},
            {'notes': 'Third order', 'status': 'shipped'},
        ]

        for data in orders_data:
            order, created = Order.objects.get_or_create(
                user=user,
                notes=data['notes'],
                defaults={'status': data['status']}
            )
            # Назначаем несколько рандомных продуктов для каждого заказа
            selected_products = random.sample(products, k=min(2, len(products)))
            order.products.set(selected_products)
            order.save()

            self.stdout.write(f"Created order #{order.id} with products {[p.name for p in selected_products]}")
