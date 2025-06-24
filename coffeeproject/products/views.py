from django.views.generic import (
    ListView,
    DetailView,
)  # Using the generic defoult views, thanks Django!
from .models import Product  # import the model!


class ProductListView(ListView):  # This is a generic option that Django offers me
    model = Product
    queryset = Product.objects.filter(is_available=True)
    paginate_by = 10


class ProductDetailView(DetailView):  # the same  as the top
    model = Product

    # def get_context_data(self, **kwargs): # -> If you need add a new field to the context
    #     return super().get_context_data(**kwargs)
