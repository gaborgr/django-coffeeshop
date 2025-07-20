from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    is_guest = models.BooleanField(default=False)
    guest_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Guest-' + self.session_key[:5]}"

    def save(self, *args, **kwargs):
        if not self.user and not self.session_key:
            raise ValueError("Guest profiles must have a session key")
        if not self.user:
            self.is_guest = True
            self.guest_expiry = timezone.now() + timezone.timedelta(days=7)
        super().save(*args, **kwargs)
