from django.test import TestCase
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
from products.models import Product
from accounts.models import Profile


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = Profile.objects.get(user=self.user)
        self.product = Product.objects.create(name="Café", price=10.0, stock=5)

    def test_order_creation(self):
        order = Order.objects.create(customer=self.profile, status="P")
        self.assertEqual(order.status, "P")
        self.assertEqual(order.total, 0)  # Verifica valor por defecto

    def test_order_item_subtotal(self):
        order = Order.objects.create(customer=self.profile)
        item = OrderItem.objects.create(
            order=order, product=self.product, quantity=2, price=10.0
        )
        self.assertEqual(item.subtotal(), 20.0)  # 2 * 10.0


class OrderSignalsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = Profile.objects.get(user=self.user)
        self.product = Product.objects.create(name="Café", price=10.0, stock=5)

    def test_signal_updates_order_total(self):
        order = Order.objects.create(customer=self.profile)
        OrderItem.objects.create(
            order=order, product=self.product, quantity=2, price=10.0
        )
        order.refresh_from_db()  # Recarga los datos desde la BD
        self.assertEqual(order.total, 20.0)  # Verifica que la señal actualizó el total
