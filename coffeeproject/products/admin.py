from django.contrib import admin
from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "stock",
        "is_available",
        "category",
        "creation_date",
    )
    list_filter = ("is_available", "category")
    list_editable = ("price", "stock", "is_available")
    search_fields = ("name", "description")
    fieldsets = (
        (None, {"fields": ("name", "description", "category")}),
        ("Price and Stock", {"fields": ("price", "stock")}),
        ("Image", {"fields": ("image",)}),
    )
