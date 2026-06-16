from rest_framework import generics

from .models import Alert
from .serializers import AlertSerializer


class AlertListCreateView(generics.ListCreateAPIView):
    serializer_class = AlertSerializer

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlertUpdateView(generics.UpdateAPIView):
    serializer_class = AlertSerializer
    http_method_names = ["patch"]

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)
