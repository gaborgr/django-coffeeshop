from django.utils import timezone
from .models import Order
from accounts.models import Profile


def get_or_create_cart(request):
    if request.user.is_authenticated:
        customer, _ = Profile.objects.get_or_create(user=request.user)
    else:
        session_key = (
            request.session.session_key or request.session.create().session_key
        )

        # Buscar o crear perfil de invitado
        customer, created = Profile.objects.get_or_create(
            session_key=session_key,
            user=None,
            defaults={
                "phone": f"guest-{session_key[:8]}",
                "address": "Guest address",
                "is_guest": True,
                "guest_expiry": timezone.now() + timezone.timedelta(days=7),
            },
        )

        # Limpiar perfiles de invitado expirados
        Profile.objects.filter(is_guest=True, guest_expiry__lt=timezone.now()).delete()

    cart, _ = Order.objects.get_or_create(
        customer=customer, status="P", defaults={"total": 0}
    )
    return cart
