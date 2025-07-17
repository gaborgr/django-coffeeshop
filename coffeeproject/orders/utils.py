from django.contrib.sessions.backends.db import SessionStore
from .models import Customer, Order


def get_or_create_cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
    else:
        # Para invitados, usamos la sesión
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        customer, created = Customer.objects.get_or_create(
            session_key=session_key, user=None
        )

    # Obtener o crear el pedido pendiente
    cart, created = Order.objects.get_or_create(customer=customer, status="P")
    return cart
