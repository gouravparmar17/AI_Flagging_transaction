from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from alerts.models import Alert
from fraud_detection.models import FraudPrediction
from .models import Transaction

User = get_user_model()


class TransactionApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", email="u1@example.com", **{"password": "StrongPass123"})
        self.other_user = User.objects.create_user(
            username="u2", email="u2@example.com", **{"password": "StrongPass123"}
        )
        login = self.client.post(
            "/api/auth/login/", {"email": "u1@example.com", "password": "StrongPass123"}, format="json"
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + login.data["access_token"])

    def test_create_transaction_auto_creates_prediction(self):
        response = self.client.post(
            "/api/transactions/",
            {"amount": 65000, "merchant": "Unknown", "location": "Unknown", "transaction_type": "Online"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 1)
        self.assertEqual(FraudPrediction.objects.filter(user=self.user).count(), 1)

    def test_user_isolation_for_transaction_detail(self):
        txn = Transaction.objects.create(
            user=self.other_user,
            amount=100,
            merchant="Shop",
            location="City",
            transaction_type="POS",
        )
        response = self.client.get(f"/api/transactions/{txn.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Alert.objects.filter(user=self.user).exists())
