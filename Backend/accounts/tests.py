from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthFlowTests(APITestCase):
    def test_register_and_login_with_email(self):
        register = self.client.post(
            "/api/auth/register/",
            {"email": "auth@example.com", "password": "StrongPass123", "full_name": "Auth User"},
            format="json",
        )
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)

        login = self.client.post(
            "/api/auth/login/", {"email": "auth@example.com", "password": "StrongPass123"}, format="json"
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", login.data)
        self.assertIn("refresh_token", login.data)
