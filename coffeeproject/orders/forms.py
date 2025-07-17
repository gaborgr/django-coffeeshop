from django import forms
from .models import OrderItem, Customer
from products.models import Product  # Importar Product para validaciones


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
                "class": "form-control",
                "max": "",  # Se establecerá dinámicamente en __init__
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
        required=True,  # Hacer obligatorio para checkout
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+56912345678"}
        ),
        help_text="Número de contacto para la entrega",
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,  # Corrección: "rows" en lugar de "row"
                "class": "form-control",
                "placeholder": "Calle, número, departamento, etc.",
            }
        ),
        required=True,
        help_text="Dirección completa para la entrega",
    )

    class Meta:
        model = Customer
        fields = ["phone", "address"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if len(phone) < 8:
            raise forms.ValidationError("Número de teléfono demasiado corto")
        return phone
