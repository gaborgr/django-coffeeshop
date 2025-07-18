from django.db.models.signals import post_save
from django.contrib.auth.models import User
from accounts.models import Profile


def create_customer(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(create_customer, sender=User)

# Crea un signal para asignar automáticamente Customer a nuevos usuarios:
