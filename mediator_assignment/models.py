"""Mediator assignment system (Section 8)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class MediatorAssignmentRequest(models.Model):
    """Mediator assignment request and selection workflow."""

    class SelectionMethod(models.TextChoices):
        PARTY_REQUESTED = "party_requested", "Party-Requested"
        MUTUAL = "mutual", "Mutual Selection"
        ADMIN_ASSIGNED = "admin_assigned", "Administrator-Assigned"
        AUTO_MATCHED = "auto_matched", "Auto-Matched by Category"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        MEDIATOR_INVITED = "mediator_invited", "Mediator Invited"
        MEDIATOR_ACCEPTED = "mediator_accepted", "Mediator Accepted"
        MEDIATOR_REJECTED = "mediator_rejected", "Mediator Rejected"
        ASSIGNMENT_CONFIRMED = "assignment_confirmed", "Assignment Confirmed"
        REPLACEMENT_REQUESTED = "replacement_requested", "Replacement Requested"
        WITHDRAWN = "withdrawn", "Withdrawn"

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="assignment_requests"
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignment_requests_made"
    )
    selection_method = models.CharField(
        max_length=30, choices=SelectionMethod.choices, default=SelectionMethod.MUTUAL
    )
    mediator = models.ForeignKey(
        "mediators.MediatorProfile", on_delete=models.PROTECT, related_name="assignment_requests"
    )
    status = models.CharField(
        max_length=30, choices=Status.choices, default=Status.PENDING
    )
    invitation_message = models.TextField(blank=True)
    proposed_fee = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    acceptance_deadline = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    confirmation_token = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Assignment {self.mediator.user.email} -> {self.dispute.case_ref}"


class MediatorReplacementRequest(models.Model):
    """Replacement request when mediator is unsuitable."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="replacement_requests"
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="replacement_requests_filed",
    )
    current_mediator = models.ForeignKey(
        "mediators.MediatorProfile",
        on_delete=models.CASCADE,
        related_name="replacement_requests_against",
    )
    reason = models.TextField()
    requested_replacement = models.ForeignKey(
        "mediators.MediatorProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replacement_requests_for",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    requested_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-requested_at"]


class AssignmentHistory(models.Model):
    """Assignment history (Section 8)."""

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="assignment_history"
    )
    mediator = models.ForeignKey(
        "mediators.MediatorProfile", on_delete=models.CASCADE
    )
    action = models.CharField(
        max_length=40,
        choices=[
            ("invited", "Invited"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
            ("confirmed", "Confirmed"),
            ("replaced", "Replaced"),
            ("withdrawn", "Withdrawn"),
        ],
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
