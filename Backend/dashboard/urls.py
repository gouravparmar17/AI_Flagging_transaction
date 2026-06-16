from django.urls import path

from .views import AnalyticsView, ChartsView, RecentAlertsView, SummaryView

urlpatterns = [
    path("summary/", SummaryView.as_view(), name="dashboard_summary"),
    path("analytics/", AnalyticsView.as_view(), name="dashboard_analytics"),
    path("charts/", ChartsView.as_view(), name="dashboard_charts"),
    path("recent-alerts/", RecentAlertsView.as_view(), name="dashboard_recent_alerts"),
]
