from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    is_avalible = models.BooleanField(default=True, verbose_name="Avalible?")
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, verbose_name="Category"
    )
    image = models.ImageField(upload_to="products/", blank=True, verbose_name="Photo")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Last Update")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    adress = models.TextField(blank=True)

    def __str__(self):
        return self.user.email


class Order(models.Model):
    STATUS_CHOICES = [("P", "Pending"), ("C", "Completed"), ("X", "Cancelled")]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"
