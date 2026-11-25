"""Grievances app - Feedback, complaint & grievance management (Section 19)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


def generate_complaint_ref():
    return f"GRV-{uuid.uuid4().hex[:10].upper()}"


class Complaint(models.Model):
    """Submit platform or mediator-related complaints (Section 19)."""

    class ComplaintType(models.TextChoices):
        PLATFORM = "platform", "Platform Issue"
        MEDIATOR_CONDUCT = "mediator_conduct", "Mediator-Related Complaint"
        OTHER_PARTY_CONDUCT = "other_party_conduct", "Other Party Conduct"
        TECHNICAL = "technical", "Technical Issue"
        BILLING = "billing", "Billing Dispute"
        PRIVACY = "privacy", "Privacy / Data Concern"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        ACKNOWLEDGED = "acknowledged", "Acknowledged"
        UNDER_INVESTIGATION = "under_investigation", "Under Investigation"
        RESOLVED = "resolved", "Resolved"
        APPEALED = "appealed", "Appealed"
        CLOSED = "closed", "Closed"
        REJECTED = "rejected", "Rejected"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    complaint_ref = models.CharField(
        max_length=40, unique=True, default=generate_complaint_ref
    )
    complainant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="complaints_filed"
    )
    complaint_type = models.CharField(
        max_length=30, choices=ComplaintType.choices, default=ComplaintType.PLATFORM
    )
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    subject = models.CharField(max_length=255)
    description = models.TextField()
    related_dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.SET_NULL, null=True, blank=True
    )
    related_mediator = models.ForeignKey(
        "mediators.MediatorProfile", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="complaints_against",
    )
    status = models.CharField(
        max_length=30, choices=Status.choices, default=Status.SUBMITTED
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_complaints",
    )
    submitted_at = models.DateTimeField(default=timezone.now)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    response_deadline = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    resolution_action = models.TextField(blank=True)
    satisfaction_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.complaint_ref} - {self.subject}"


class ComplaintResponse(models.Model):
    """Responses / investigation records on a complaint."""

    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name="responses"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    response_text = models.TextField()
    is_internal_note = models.BooleanField(default=False)
    is_official_response = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]


class ComplaintAppeal(models.Model):
    """Appeal or review requests on resolved complaints (Section 19)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    original_complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name="appeals"
    )
    appellant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="complaint_appeals_filed",
    )
    reason = models.TextField()
    requested_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="complaint_appeals_reviewed",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    decision_notes = models.TextField(blank=True)


class Feedback(models.Model):
    """Service quality feedback / mediator feedback (Section 19)."""

    class FeedbackType(models.TextChoices):
        PLATFORM = "platform", "Platform Feedback"
        MEDIATOR = "mediator", "Mediator Feedback"
        CASE_OUTCOME = "case_outcome", "Case Outcome Feedback"
        GENERAL = "general", "General Feedback"

    feedback_type = models.CharField(
        max_length=30, choices=FeedbackType.choices, default=FeedbackType.PLATFORM
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="feedbacks_given",
    )
    related_dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.SET_NULL, null=True, blank=True
    )
    related_mediator = models.ForeignKey(
        "mediators.MediatorProfile", on_delete=models.SET_NULL, null=True, blank=True
    )
    rating = models.PositiveSmallIntegerField()
    ease_of_use_rating = models.PositiveSmallIntegerField(default=0)
    speed_rating = models.PositiveSmallIntegerField(default=0)
    fairness_rating = models.PositiveSmallIntegerField(default=0)
    comments = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-submitted_at"]


class GrievanceInvestigation(models.Model):
    """Grievance investigation records (Section 19)."""

    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name="investigations"
    )
    investigator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    findings = models.TextField(blank=True)
    recommended_action = models.TextField(blank=True)
    supporting_documents = models.ManyToManyField(
        "documents.Document", related_name="linked_grievance_investigations", blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("suspended", "Suspended"),
        ],
        default="in_progress",
    )
