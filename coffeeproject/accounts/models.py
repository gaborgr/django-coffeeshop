from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    # Más campos si necesitas (ej: birth_date, avatar)

    def __str__(self):
        return f"Perfil de {self.user.email}"
