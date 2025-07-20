from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente
            return redirect(
                "product-list"
            )  # Redirige a la página principal MODIFICAR AL CREAR EL HOME
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


class LoginOrGuestView(FormView):
    template_name = "accounts/login_or_guest.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("product-list")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "")
        return context
