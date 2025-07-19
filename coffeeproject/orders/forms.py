from django import forms
from .models import OrderItem
from accounts.models import Profile


class AddToCartForm(forms.ModelForm):
    """
    Form to add products to the Cart.
    Price is set via signals, but we add stock validation here.
    """

    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "class": "w-20 px-3 py-2 border border-gray-300 rounded-md text-center focus:outline-none focus:ring-amber-500 focus:border-amber-500",
            }
        ),
    )

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop("product", None)  # Guardar product como atributo
        super().__init__(*args, **kwargs)
        if self.product:
            self.fields["product"].initial = self.product
            self.fields["product"].widget = forms.HiddenInput()
            # Establecer máximo según stock disponible
            self.fields["quantity"].widget.attrs["max"] = self.product.stock

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if self.product and quantity > self.product.stock:
            raise forms.ValidationError(
                f"No hay suficiente stock. Disponible: {self.product.stock}"
            )
        return quantity


class CheckoutForm(forms.ModelForm):
    """
    Customer data with improved validation.
    """

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-amber-500 focus:border-amber-500",
                "placeholder": "+56912345678",
            }
        ),
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-amber-500 focus:border-amber-500",
                "rows": 3,
                "placeholder": "Calle, número, departamento, etc.",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["phone", "address"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if len(phone) < 8:
            raise forms.ValidationError("Número de teléfono demasiado corto")
        return phone
