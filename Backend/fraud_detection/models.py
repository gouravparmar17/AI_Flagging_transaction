from django.conf import settings
from django.db import models


class FraudPrediction(models.Model):
    class PredictionChoices(models.TextChoices):
        FRAUD = "Fraud", "Fraud"
        SAFE = "Safe", "Safe"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fraud_predictions")
    transaction = models.ForeignKey(
        "transactions.Transaction", on_delete=models.CASCADE, related_name="predictions", null=True, blank=True
    )
    fraud_probability = models.FloatField()
    risk_score = models.PositiveIntegerField()
    confidence = models.FloatField()
    prediction = models.CharField(max_length=10, choices=PredictionChoices.choices)
    model_version = models.CharField(max_length=50, default="v1")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
