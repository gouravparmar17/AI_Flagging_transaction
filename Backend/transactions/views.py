from rest_framework import generics, status
from rest_framework.response import Response

from fraud_detection.services import create_prediction_for_transaction

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(user=request.user)
        prediction, score = create_prediction_for_transaction(request.user, transaction)
        payload = {
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
        return Response(payload, status=status.HTTP_201_CREATED)


class TransactionDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
