from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_profile_creation_via_signal(self):
        # La señal debería crear automáticamente un Profile
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, "testuser")


class RegistrationTest(TestCase):
    def test_register_view(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "complexpass123",
                "password2": "complexpass123",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirección después de registro
        self.assertRedirects(
            response, reverse("product-list")
        )  # modificar esto cuando tenga un home creado
        self.assertTrue(User.objects.filter(username="newuser").exists())
