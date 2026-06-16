from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/transactions/", include("transactions.urls")),
    path("api/fraud/", include("fraud_detection.urls")),
    path("api/dashboard/", include("dashboard.urls")),
    path("api/reports/", include("reports.urls")),
    path("api/alerts/", include("alerts.urls")),
]
