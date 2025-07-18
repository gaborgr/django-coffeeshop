from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)  # Campo extra

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "phone"]
