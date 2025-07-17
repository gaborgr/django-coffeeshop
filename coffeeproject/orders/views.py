from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from .utils import get_or_create_cart
from .forms import AddToCartForm, CheckoutForm
from .models import OrderItem


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = get_or_create_cart(request)  # Usamos la función helper

    if request.method == "POST":
        form = AddToCartForm(request.POST, product=product)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            # Validar stock
            if quantity > product.stock:
                form.add_error("quantity", "No hay suficiente stock")
            else:
                # Añadir al carrito
                order_item, created = OrderItem.objects.get_or_create(
                    order=cart,
                    product=product,
                    defaults={"quantity": quantity, "price": product.price},
                )
                if not created:
                    order_item.quantity += quantity
                    order_item.save()
                return redirect("cart_view")
    else:
        form = AddToCartForm(product=product)

    return render(
        request, "orders/add_to_cart.html", {"form": form, "product": product}
    )


def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.orderitem_set.all()  # Items del carrito

    return render(request, "orders/cart.html", {"cart": cart, "items": items})


def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.orderitem_set.exists():
        return redirect("cart_view")  # No permitir checkout si el carrito está vacío

    if request.method == "POST":
        form = CheckoutForm(request.POST, instance=cart.customer)
        if form.is_valid():
            form.save()
            cart.status = "C"  # Marcar como completado
            cart.save()
            return redirect("order_confirmation")
    else:
        form = CheckoutForm(instance=cart.customer)

    return render(request, "orders/checkout.html", {"form": form})
