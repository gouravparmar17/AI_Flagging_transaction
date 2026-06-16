from django.conf import settings
from django.db import models


class Alert(models.Model):
    class SeverityChoices(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"
        CRITICAL = "Critical", "Critical"

    class StatusChoices(models.TextChoices):
        OPEN = "Open", "Open"
        REVIEWING = "Reviewing", "Reviewing"
        RESOLVED = "Resolved", "Resolved"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="alerts")
    transaction = models.ForeignKey(
        "transactions.Transaction", on_delete=models.CASCADE, related_name="alerts", null=True, blank=True
    )
    severity = models.CharField(max_length=10, choices=SeverityChoices.choices)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
