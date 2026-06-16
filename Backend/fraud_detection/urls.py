from django.urls import path

from .views import PredictFraudView, PredictionDetailView, PredictionListView

urlpatterns = [
    path("predict/", PredictFraudView.as_view(), name="predict_fraud"),
    path("predictions/", PredictionListView.as_view(), name="prediction_list"),
    path("predictions/<int:pk>/", PredictionDetailView.as_view(), name="prediction_detail"),
]
