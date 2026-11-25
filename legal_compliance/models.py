"""Legal compliance app (Section 20)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class ConsentRecord(models.Model):
    """Consent management (Section 20)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consents"
    )
    consent_type = models.CharField(
        max_length=40,
        choices=[
            ("terms_of_service", "Terms of Service"),
            ("privacy_policy", "Privacy Policy"),
            ("marketing", "Marketing Communications"),
            ("whatsapp", "WhatsApp Communications"),
            ("data_processing", "Data Processing"),
            ("recording", "Session Recording"),
            ("kyc", "KYC Verification"),
            ("disclosure", "Information Disclosure"),
        ],
    )
    consent_version = models.CharField(max_length=30, default="1.0")
    is_given = models.BooleanField(default=False)
    given_at = models.DateTimeField(null=True, blank=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ["-given_at"]


class DataSubjectRequest(models.Model):
    """Data deletion requests / data subject rights (Section 20)."""

    class RequestType(models.TextChoices):
        ACCESS = "access", "Data Access Request"
        CORRECTION = "correction", "Data Correction Request"
        DELETION = "deletion", "Data Deletion Request"
        PORTABILITY = "portability", "Data Portability Request"
        RESTRICTION = "restriction", "Data Processing Restriction"
        OBJECTION = "objection", "Objection to Processing"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Identity Verified"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="data_subject_requests",
    )
    request_type = models.CharField(max_length=30, choices=RequestType.choices)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    requested_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_data_requests",
    )
    admin_notes = models.TextField(blank=True)


class DataRetentionPolicy(models.Model):
    """Data retention policies (Section 20)."""

    category = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    retention_period_days = models.PositiveIntegerField(default=2555)  # 7 years default
    auto_delete = models.BooleanField(default=False)
    legal_basis = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)


class SecurityIncident(models.Model):
    """Security incident management (Section 20)."""

    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class Status(models.TextChoices):
        REPORTED = "reported", "Reported"
        INVESTIGATING = "investigating", "Investigating"
        CONTAINED = "contained", "Contained"
        RESOLVED = "resolved", "Resolved"
        ESCALATED = "escalated", "Escalated"

    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(
        max_length=10, choices=Severity.choices, default=Severity.MEDIUM
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.REPORTED
    )
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reported_incidents",
    )
    affected_users_count = models.PositiveIntegerField(default=0)
    affected_disputes_count = models.PositiveIntegerField(default=0)
    detected_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_summary = models.TextField(blank=True)
    notification_sent_to_users = models.BooleanField(default=False)
    notification_sent_to_authority = models.BooleanField(default=False)
    is_publicly_disclosed = models.BooleanField(default=False)


class ConflictOfInterestDeclaration(models.Model):
    """User-declared conflict-of-interest (Section 20)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="user_coi_declarations"
    )
    related_dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, null=True, blank=True
    )
    has_conflict = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    declared_at = models.DateTimeField(default=timezone.now)
    resolution = models.CharField(
        max_length=30,
        choices=[
            ("recused", "Recused"),
            ("disclosed_and_proceeded", "Disclosed & Proceeded"),
            ("withdrawn", "Withdrawn"),
        ],
        blank=True,
    )
