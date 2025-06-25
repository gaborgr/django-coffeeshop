from django.test import TestCase
from django.urls import reverse
from .models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Donuts", slug="donuts")

    def test_category_creation(self):
        """Testing the category creation it's ok"""
        self.assertEqual(self.category.name, "Donuts")
        self.assertEqual(self.category.slug, "donuts")

    def test_category_str_representation(self):
        """Check if __str__ return the name"""
        self.assertEqual(str(self.category), "Donuts")

    # def test_slug_is_unique(slef):
    #     with self.assertRaises(Exception):
    #         Category.objects.create(name="Donuts", slug="donuts")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Donuts", slug="donuts")
        self.product = Product.objects.create(
            name="Babarian Donut",
            description="Best donut ever",
            price=2.50,
            stock=10,
            is_available=True,
            category=self.category,
        )

    def test_product_creation(self):
        """Test the product creation ok"""
        self.assertEqual(self.product.name, "Babarian Donut")
        self.assertEqual(self.product.price, 2.50)
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(self.product.is_available)
        self.assertEqual(self.product.category.name, "Donuts")

    def test_str_representation(self):
        """Test that __str__ return the name"""
        self.assertEqual(str(self.product), "Babarian Donut")

    def test_get_absolute_url(self):
        """Test the method to redirect to detail template"""
        url = reverse("product-detail", kwargs={"pk": self.product.pk})
        self.assertEqual(self.product.get_absolute_url(), url)

    def test_default_values(self):
        """Test the dates fields creation_date and last_update"""
        self.assertIsNotNone(self.product.creation_date)
        self.assertIsNotNone(self.product.last_update)

    def test_optional_fields(self):
        """Test the optional fields (blank=True) like description"""
        product_without_desc = Product.objects.create(
            name="Matcha", price=1.50, category=self.category
        )
        self.assertEqual(product_without_desc.description, "")

    def test_category_deletion(self):
        """Test when eliminate a category the products field chance to None (SET_NULL)"""
        self.category.delete()
        self.product.refresh_from_db()
        self.assertIsNone(self.product.category)
