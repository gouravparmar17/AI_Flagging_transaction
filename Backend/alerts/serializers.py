from rest_framework import serializers

from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    transaction_id = serializers.CharField(source="transaction.transaction_id", read_only=True)

    class Meta:
        model = Alert
        fields = ["id", "transaction", "transaction_id", "severity", "status", "created_at"]
        read_only_fields = ["id", "created_at", "transaction_id"]
