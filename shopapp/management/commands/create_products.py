from django.core.management.base import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    help = "Create sample products"

    def handle(self, *args, **kwargs):
        products_data = [
            {'name': 'Product A', 'description': 'Description A', 'price': 10.99, 'quantity': 100, 'is_active': True},
            {'name': 'Product B', 'description': 'Description B', 'price': 5.50, 'quantity': 50, 'is_active': True},
            {'name': 'Product C', 'description': 'Description C', 'price': 20.00, 'quantity': 10, 'is_active': False},
        ]

        for pdata in products_data:
            product, created = Product.objects.get_or_create(
                name=pdata['name'],
                defaults=pdata
            )
            if created:
                self.stdout.write(f"Created product: {product.name}")
            else:
                self.stdout.write(f"Product already exists: {product.name}")
