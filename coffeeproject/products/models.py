from django.db import models
from django.urls import reverse  # you need this to move into the product detail


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    is_available = models.BooleanField(default=True, verbose_name="Available?")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name="Category"
    )
    image = models.ImageField(upload_to="products/", blank=True, verbose_name="Photo")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Last Update")

    def get_absolute_url(self):
        return reverse(
            "product-detail", kwargs={"pk": self.pk}
        )  # go to the template detail product

    def __str__(self):
        return self.name
