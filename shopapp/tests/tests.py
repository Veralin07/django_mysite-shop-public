from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from shopapp.models import Order

class OrdersExportTestCase(TestCase):
    fixtures = ['users.json', 'products.json', 'orders.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(username='staffuser', password='pass', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.staff_user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.login(username='staffuser', password='pass')

    def test_orders_export_json(self):
        url = reverse('shopapp:orders_export')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn('orders', data)

        # Формируем ожидаемые данные из базы
        orders_qs = Order.objects.prefetch_related('products').all()
        expected_orders = []
        for order in orders_qs:
            expected_orders.append({
                'id': order.id,
                'address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user.id,
                'product_ids': list(order.products.values_list('id', flat=True)),
            })

        # Сравниваем списки без учёта порядка
        self.assertCountEqual(data['orders'], expected_orders)