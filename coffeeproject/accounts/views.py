from django.shortcuts import render, redirect
from django.contrib.auth import login
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
