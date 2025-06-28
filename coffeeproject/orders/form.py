from django import forms
from products.models import Product
from .models import Order, OrderItem, Customer


class AddToCartForm(forms.ModelForm):
    """
    Form to add products to the Cart
    prices comes via signals from Products
    """

    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]  # price adding auto

    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields["product"].initial = product
            self.fields["product"].widget = forms.HiddenInput()


class CheckoutForm(forms.ModelForm):
    """
    Customer data
    """

    class Model:
        model = Customer
        fields = ["phone", "address"]
        widgets = {
            "address": forms.Textarea(attrs={"row": 3, "class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }
