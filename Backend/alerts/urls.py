from django.urls import path

from .views import AlertListCreateView, AlertUpdateView

urlpatterns = [
    path("", AlertListCreateView.as_view(), name="alerts_list_create"),
    path("<int:pk>/", AlertUpdateView.as_view(), name="alerts_update"),
]
