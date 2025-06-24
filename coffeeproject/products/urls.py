from django.urls import path
from .views import ProductDetailView, ProductListView  # Bring those views!

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),  # The main product list
    path(
        "<int:pk>", ProductDetailView.as_view(), name="product-detail"
    ),  # The product Detail, can be slug but you need add the field at the model
]
