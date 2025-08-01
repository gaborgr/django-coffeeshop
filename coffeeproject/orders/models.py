from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from products.models import Product
from accounts.models import Profile


class Order(models.Model):
    STATUS_CHOICES = [("P", "Pending"), ("C", "Completed"), ("X", "Cancelled")]
    customer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "orders_order"

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

    def update_total(self):
        self.total = sum(
            item.subtotal() for item in self.orderitem_set.all()
        )  # Usa subtotal()
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])
    price = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.quantity} x {self.product} (Order #{self.order.id})"

    def subtotal(self):
        return self.quantity * self.price


# ------------------------------- SIGNALS -------------------------------
@receiver(pre_save, sender=OrderItem)
def set_order_item_price(sender, instance, **kwargs):
    if not instance.price:
        instance.price = instance.product.price


@receiver(post_save, sender=OrderItem)
def update_order_total_on_item_change(sender, instance, **kwargs):
    instance.order.update_total()
