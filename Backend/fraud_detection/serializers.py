from rest_framework import serializers

from .models import FraudPrediction
from .services import FraudScoringService


class FraudPredictionSerializer(serializers.ModelSerializer):
    transaction_id = serializers.CharField(source="transaction.transaction_id", read_only=True)

    class Meta:
        model = FraudPrediction
        fields = [
            "id",
            "transaction_id",
            "fraud_probability",
            "risk_score",
            "confidence",
            "prediction",
            "model_version",
            "created_at",
        ]


class PredictInputSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    merchant = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    transaction_type = serializers.CharField(max_length=100)
    device_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    ip_address = serializers.CharField(max_length=45, required=False, allow_blank=True)

    def to_representation(self, instance):
        return FraudScoringService.score(instance)
