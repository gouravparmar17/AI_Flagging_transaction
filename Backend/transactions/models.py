import uuid

from django.conf import settings
from django.db import models


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    transaction_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    merchant = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=100)
    device_id = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
