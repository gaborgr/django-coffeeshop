from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from products.models import Product
from .utils import get_or_create_cart
from .forms import AddToCartForm, CheckoutForm
from .models import OrderItem, Order


def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.orderitem_set.all()  # Items del carrito

    return render(
        request,
        "orders/cart.html",
        {"cart": cart, "cart_items": cart.orderitem_set.all()},
    )


@require_POST
def continue_as_guest(request):
    # 1. Forzar creación de sesión si no existe
    if not request.session.session_key:
        request.session.create()

    # 2. Manejar producto pendiente si existe
    product_id = request.session.pop("pending_product", None)
    if product_id:
        try:
            product = Product.objects.get(id=product_id, is_available=True)
            cart = get_or_create_cart(request)

            # Añadir producto al carrito (lógica similar a add_to_cart)
            order_item, created = OrderItem.objects.get_or_create(
                order=cart,
                product=product,
                defaults={"quantity": 1, "price": product.price},
            )
            if not created:
                order_item.quantity += 1
                order_item.save()
        except Product.DoesNotExist:
            pass

    # 3. Redirigir al destino original o al carrito
    next_url = request.POST.get("next") or "cart-view"
    return redirect(next_url)


def add_to_cart(request, product_id):
    # Verificar autenticación primero
    if not request.user.is_authenticated:
        # Guardar producto en sesión y redirigir a login especial
        request.session["pending_product"] = product_id
        redirect_url = reverse("accounts:login-or-guest")
        next_url = reverse("orders:add-to-cart", args=[product_id])
        return redirect(f"{redirect_url}?next={next_url}")

    # Lógica para usuarios autenticados
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = get_or_create_cart(request)

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
                return redirect("orders:cart-view")
    else:
        form = AddToCartForm(product=product)

    return render(
        request, "orders/add_to_cart.html", {"form": form, "product": product}
    )


def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.orderitem_set.exists():
        return redirect("orders:cart-view")

    if request.method == "POST":
        form = CheckoutForm(request.POST, instance=cart.customer)
        if form.is_valid():
            # Guardar información del cliente
            customer = form.save(commit=False)
            if not request.user.is_authenticated:
                customer.session_key = request.session.session_key
            customer.save()

            # Completar el pedido
            cart.status = "C"
            cart.customer = customer
            cart.save()

            return redirect("orders:order-confirmation", order_id=cart.id)

    else:
        form = CheckoutForm(instance=cart.customer)

    return render(
        request,
        "orders/checkout.html",
        {"form": form, "cart": cart, "cart_items": cart.orderitem_set.all()},
    )


def order_confirmation(request, order_id):
    """
    Vista para mostrar la confirmación del pedido.
    Para usuarios autenticados: verifica que el pedido les pertenezca
    Para invitados: verifica la sesión actual
    """
    if request.user.is_authenticated:
        # Usuario registrado - buscar pedido por usuario
        order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    else:
        # Usuario invitado - buscar pedido por sesión
        session_key = request.session.session_key
        if not session_key:
            return redirect("products:product-list")  # No hay sesión, redirigir

        order = get_object_or_404(
            Order,
            id=order_id,
            customer__session_key=session_key,
            status="C",  # Solo pedidos completados
        )

    return render(request, "orders/order_confirmation.html", {"order": order})


def increase_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__status="P")
    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()
    return redirect("cart-view")


def decrease_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__status="P")
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect("cart-view")


def remove_from_cart(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__status="P")
    item.delete()
    return redirect("cart-view")
