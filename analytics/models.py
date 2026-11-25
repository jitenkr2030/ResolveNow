"""Analytics app - ODR analytics (Section 21)."""
from django.db import models
from django.conf import settings
from django.utils import timezone


class AnalyticsSnapshot(models.Model):
    """Periodic platform-wide analytics snapshot."""

    snapshot_date = models.DateField(default=timezone.now)
    total_users = models.PositiveIntegerField(default=0)
    total_mediators = models.PositiveIntegerField(default=0)
    total_disputes = models.PositiveIntegerField(default=0)
    active_cases = models.PositiveIntegerField(default=0)
    resolved_cases = models.PositiveIntegerField(default=0)
    withdrawn_cases = models.PositiveIntegerField(default=0)
    total_disputed_value = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    avg_resolution_days = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    new_disputes_today = models.PositiveIntegerField(default=0)
    closed_disputes_today = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-snapshot_date"]


class CategoryAnalytics(models.Model):
    """Dispute category-level analytics."""

    category = models.ForeignKey(
        "dispute_categories.DisputeCategory", on_delete=models.CASCADE
    )
    snapshot_date = models.DateField(default=timezone.now)
    total_disputes = models.PositiveIntegerField(default=0)
    resolved_count = models.PositiveIntegerField(default=0)
    avg_resolution_days = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_disputed_value = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    mediator_workload = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ["-snapshot_date"]


class MediatorPerformanceMetric(models.Model):
    """Mediator workload and performance analytics (Section 21)."""

    mediator = models.ForeignKey(
        "mediators.MediatorProfile", on_delete=models.CASCADE, related_name="metrics"
    )
    period_start = models.DateField()
    period_end = models.DateField()
    assigned_cases = models.PositiveIntegerField(default=0)
    completed_cases = models.PositiveIntegerField(default=0)
    successful_settlements = models.PositiveIntegerField(default=0)
    unsuccessful_cases = models.PositiveIntegerField(default=0)
    avg_session_duration_minutes = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    avg_rating = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    revenue_generated = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    workload_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
