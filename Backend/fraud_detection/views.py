from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FraudPrediction
from .serializers import FraudPredictionSerializer, PredictInputSerializer
from .services import FraudScoringService


class PredictFraudView(APIView):
    def post(self, request):
        serializer = PredictInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        score = FraudScoringService.score(serializer.validated_data)
        return Response(score, status=status.HTTP_200_OK)


class PredictionListView(generics.ListAPIView):
    serializer_class = FraudPredictionSerializer

    def get_queryset(self):
        return FraudPrediction.objects.filter(user=self.request.user)


class PredictionDetailView(generics.RetrieveAPIView):
    serializer_class = FraudPredictionSerializer

    def get_queryset(self):
        return FraudPrediction.objects.filter(user=self.request.user)
