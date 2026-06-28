from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["email"]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audit_logs")
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
