"""Case management app (Section 4) - additional case-management features."""
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import PermissionDenied


class CaseTransfer(models.Model):
    """Case transfer / reassignment history."""

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="transfers"
    )
    transferred_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transfers_initiated",
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transfers_from",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transfers_to",
    )
    reason = models.TextField()
    transferred_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-transferred_at"]

    def __str__(self):
        return f"Transfer of {self.dispute.case_ref}"


class CaseWithdrawalRequest(models.Model):
    """Case withdrawal requests."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="withdrawal_requests"
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="withdrawal_requests_requested",
    )
    reason = models.TextField()
    requested_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="withdrawal_requests_reviewed",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-requested_at"]


class CaseReopeningRequest(models.Model):
    """Reopening requests for closed cases (Section 4)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="reopening_requests"
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reopening_requests_requested",
    )
    reason = models.TextField()
    requested_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reopening_requests_reviewed",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    new_status = models.CharField(max_length=40, blank=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-requested_at"]


class CaseReminder(models.Model):
    """Case deadlines and reminders (Section 4)."""

    class ReminderType(models.TextChoices):
        RESPONSE_DEADLINE = "response_deadline", "Response Deadline"
        NEGOTIATION_DEADLINE = "negotiation_deadline", "Negotiation Deadline"
        SESSION_REMINDER = "session_reminder", "Session Reminder"
        DOCUMENT_DEADLINE = "document_deadline", "Document Submission Deadline"
        PAYMENT_DEADLINE = "payment_deadline", "Payment Deadline"
        SETTLEMENT_DEADLINE = "settlement_deadline", "Settlement Deadline"

    dispute = models.ForeignKey(
        "disputes.Dispute",
        on_delete=models.CASCADE,
        related_name="reminders",
    )
    reminder_type = models.CharField(max_length=30, choices=ReminderType.choices)
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="case_reminders"
    )
    due_at = models.DateTimeField()
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_acknowledged = models.BooleanField(default=False)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["due_at"]


class CaseNote(models.Model):
    """Internal administrative notes (Section 4) - separate from timeline."""

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="admin_notes"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.TextField()
    is_internal = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class CaseArchive(models.Model):
    """Archive and retrieval of closed cases (Section 4)."""

    dispute = models.OneToOneField(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="archive_record"
    )
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    archived_at = models.DateTimeField(default=timezone.now)
    archive_reason = models.TextField(blank=True)
    is_retrievable = models.BooleanField(default=True)
    retrieval_requested = models.BooleanField(default=False)
    retrieval_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-archived_at"]
