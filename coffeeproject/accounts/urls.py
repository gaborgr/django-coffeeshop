from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register
from .forms import CustomLoginForm

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html", form_class=CustomLoginForm
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
]
