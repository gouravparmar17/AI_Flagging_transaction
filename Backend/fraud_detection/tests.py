from django.contrib.auth import get_user_model
from django.test import TestCase

from transactions.models import Transaction
from .services import create_prediction_for_transaction

User = get_user_model()


class FraudServiceTests(TestCase):
    def test_create_prediction_for_transaction(self):
        user = User.objects.create_user(username="fs", email="fs@example.com", **{"password": "StrongPass123"})
        txn = Transaction.objects.create(user=user, amount=1200, merchant="Amazon", location="Indore", transaction_type="POS")
        prediction, score = create_prediction_for_transaction(user, txn)
        self.assertEqual(prediction.user, user)
        self.assertIn(score["prediction"], ["Fraud", "Safe"])
