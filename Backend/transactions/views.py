from rest_framework import generics, status
from rest_framework.response import Response

from fraud_detection.services import create_prediction_for_transaction

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    prediction_payload = None

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)
        prediction, score = create_prediction_for_transaction(self.request.user, transaction)
        self.prediction_payload = {
            "transaction": TransactionSerializer(transaction).data,
            "prediction": {
                "id": prediction.id,
                "prediction": score["prediction"],
                "fraud_probability": score["fraud_probability"],
                "risk_score": score["risk_score"],
                "confidence": score["confidence"],
                "severity": score["severity"],
            },
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if self.prediction_payload is None:
            return response
        return Response(self.prediction_payload, status=status.HTTP_201_CREATED)


class TransactionDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
