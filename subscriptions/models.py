"""Subscriptions app - Subscription management (Section 17 - corporate)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Subscription(models.Model):
    """Active subscription for an organization."""

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="subscription_records"
    )
    plan = models.ForeignKey(
        "payments.SubscriptionPlan", on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("trial", "Trial"),
            ("suspended", "Suspended"),
            ("cancelled", "Cancelled"),
            ("expired", "Expired"),
        ],
        default="active",
    )
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    auto_renew = models.BooleanField(default=True)
    monthly_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cases_used_this_month = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)


class APIKey(models.Model):
    """API integrations for business/corporate portal (Section 17)."""

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="api_keys"
    )
    key_name = models.CharField(max_length=80)
    api_key = models.CharField(max_length=128, unique=True)
    key_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    permissions = models.JSONField(default=list)
    last_used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)


class BulkDisputeImport(models.Model):
    """Bulk dispute registration for corporate portal (Section 17)."""

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="bulk_imports"
    )
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="bulk_imports/", max_length=500)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("processing", "Processing"),
                 ("completed", "Completed"), ("failed", "Failed")],
        default="pending",
    )
    total_rows = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_log = models.TextField(blank=True)
