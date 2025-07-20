from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.cart_view, name="cart-view"),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "order-confirmation/<int:order_id>/",
        views.order_confirmation,
        name="order-confirmation",
    ),
    path("increase/<int:item_id>/", views.increase_quantity, name="increase-quantity"),
    path("decrease/<int:item_id>/", views.decrease_quantity, name="decrease-quantity"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove-from-cart"),
    path("continue-as-guest/", views.continue_as_guest, name="continue-as-guest"),
]
