from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "transaction_id",
            "amount",
            "merchant",
            "location",
            "transaction_type",
            "device_id",
            "ip_address",
            "timestamp",
        ]
        read_only_fields = ["id", "transaction_id", "timestamp"]
