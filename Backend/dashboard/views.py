from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncWeek
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.models import Alert
from fraud_detection.models import FraudPrediction
from transactions.models import Transaction


class SummaryView(APIView):
    def get(self, request):
        txs = Transaction.objects.filter(user=request.user)
        predictions = FraudPrediction.objects.filter(user=request.user)
        total = txs.count()
        fraud_count = predictions.filter(prediction="Fraud").count()
        safe_count = max(total - fraud_count, 0)
        fraud_percentage = round((fraud_count / total) * 100, 2) if total else 0.0
        return Response(
            {
                "total_transactions": total,
                "fraud_count": fraud_count,
                "safe_count": safe_count,
                "fraud_percentage": fraud_percentage,
            }
        )


class AnalyticsView(APIView):
    def get(self, request):
        txs = Transaction.objects.filter(user=request.user)
        monthly = (
            txs.annotate(period=TruncMonth("timestamp"))
            .values("period")
            .annotate(count=Count("id"))
            .order_by("period")
        )
        weekly = (
            txs.annotate(period=TruncWeek("timestamp"))
            .values("period")
            .annotate(count=Count("id"))
            .order_by("period")
        )
        return Response(
            {
                "monthly_trend": [
                    {"period": item["period"].date().isoformat() if item["period"] else None, "count": item["count"]}
                    for item in monthly
                ],
                "weekly_trend": [
                    {"period": item["period"].date().isoformat() if item["period"] else None, "count": item["count"]}
                    for item in weekly
                ],
            }
        )


class ChartsView(APIView):
    def get(self, request):
        predictions = FraudPrediction.objects.filter(user=request.user)
        risk_distribution = {
            "safe": predictions.filter(risk_score__lt=50).count(),
            "review": predictions.filter(risk_score__gte=50, risk_score__lt=75).count(),
            "critical": predictions.filter(risk_score__gte=75).count(),
        }
        transaction_volume = list(
            Transaction.objects.filter(user=request.user)
            .annotate(period=TruncMonth("timestamp"))
            .values("period")
            .annotate(count=Count("id"))
            .order_by("period")
        )
        return Response(
            {
                "transaction_volume": [
                    {"period": item["period"].date().isoformat() if item["period"] else None, "count": item["count"]}
                    for item in transaction_volume
                ],
                "risk_distribution": risk_distribution,
            }
        )


class RecentAlertsView(APIView):
    def get(self, request):
        alerts = Alert.objects.filter(user=request.user).values("id", "severity", "status", "created_at")[:10]
        return Response({"recent_alerts": list(alerts)})
