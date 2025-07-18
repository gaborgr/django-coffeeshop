from django.contrib import admin
from .models import Order


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "total", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer__user__email", "id")
    readonly_fields = ("created_at",)
