"""Disputes app - Dispute registration and case filing (Section 2)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid
import hashlib
import time


def generate_case_reference():
    """Generate unique case reference number RN-YYYY-XXXXXX."""
    from django.conf import settings as dj_settings

    prefix = dj_settings.RESOLVENOW_CONFIG.get("CASE_REF_PREFIX", "RN")
    year = timezone.now().year
    random_part = uuid.uuid4().hex[:6].upper()
    return f"{prefix}-{year}-{random_part}"


class Dispute(models.Model):
    """Dispute / case core record (Section 2 & 4).

    A dispute is filed by a claimant against one or more respondents.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        UNDER_REVIEW = "under_review", "Under Review"
        AWAITING_PARTY_RESPONSE = "awaiting_party_response", "Awaiting Party Response"
        ELIGIBLE_FOR_MEDIATION = "eligible_for_mediation", "Eligible for Mediation"
        MEDIATOR_ASSIGNMENT = "mediator_assignment", "Mediator Assignment"
        NEGOTIATION_IN_PROGRESS = "negotiation_in_progress", "Negotiation in Progress"
        MEDIATION_SCHEDULED = "mediation_scheduled", "Mediation Scheduled"
        MEDIATION_IN_PROGRESS = "mediation_in_progress", "Mediation in Progress"
        SETTLEMENT_PROPOSED = "settlement_proposed", "Settlement Proposed"
        SETTLEMENT_ACCEPTED = "settlement_accepted", "Settlement Accepted"
        CLOSED = "closed", "Closed"
        WITHDRAWN = "withdrawn", "Withdrawn"
        UNRESOLVED = "unresolved", "Unresolved"
        REJECTED = "rejected", "Rejected"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    case_ref = models.CharField(max_length=40, unique=True, default=generate_case_reference)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        "dispute_categories.DisputeCategory",
        on_delete=models.PROTECT,
        related_name="disputes",
    )
    sub_category = models.CharField(max_length=120, blank=True)

    # Parties
    claimant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="filed_disputes",
        help_text="Primary claimant / filer",
    )
    claimant_organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="filed_disputes",
    )
    representing_lawyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="represented_disputes",
    )

    # Amount
    disputed_amount = models.DecimalField(
        max_digits=16, decimal_places=2, default=0
    )
    currency = models.CharField(max_length=10, default="INR")
    is_amount_confidential = models.BooleanField(default=False)

    # Details (Section 2)
    agreement_reference = models.CharField(max_length=160, blank=True)
    agreement_date = models.DateField(null=True, blank=True)
    agreement_summary = models.TextField(blank=True)
    previous_communication_history = models.TextField(blank=True)
    requested_resolution = models.TextField()
    jurisdiction = models.CharField(max_length=120, default="India")
    location_of_dispute = models.CharField(max_length=160, blank=True)

    # Workflow
    status = models.CharField(
        max_length=40, choices=Status.choices, default=Status.DRAFT
    )
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    is_draft = models.BooleanField(default=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    closure_reason = models.TextField(blank=True)
    is_confidential = models.BooleanField(default=True)

    # Case management (Section 4)
    assigned_case_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_disputes",
    )
    assigned_mediator = models.ForeignKey(
        "mediators.MediatorProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_disputes",
    )
    internal_notes = models.TextField(blank=True, help_text="Internal admin notes.")

    # Deadlines
    response_deadline = models.DateTimeField(null=True, blank=True)
    negotiation_deadline = models.DateTimeField(null=True, blank=True)
    overall_deadline = models.DateTimeField(null=True, blank=True)

    # Soft retrieval
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Dispute"
        verbose_name_plural = "Disputes"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["category"]),
            models.Index(fields=["assigned_mediator"]),
        ]

    def __str__(self):
        return f"{self.case_ref} - {self.title[:60]}"

    def save(self, *args, **kwargs):
        if self.status == self.Status.SUBMITTED and not self.submitted_at:
            self.submitted_at = timezone.now()
            self.is_draft = False
            if not self.response_deadline:
                from django.conf import settings
                days = settings.RESOLVENOW_CONFIG["RESPONSE_DEADLINE_DAYS"]
                self.response_deadline = timezone.now() + timezone.timedelta(days=days)
            if not self.negotiation_deadline:
                from django.conf import settings
                days = settings.RESOLVENOW_CONFIG["NEGOTIATION_DEADLINE_DAYS"]
                self.negotiation_deadline = timezone.now() + timezone.timedelta(days=days)
        if self.status in {
            self.Status.CLOSED,
            self.Status.WITHDRAWN,
            self.Status.UNRESOLVED,
            self.Status.REJECTED,
        } and not self.closed_at:
            self.closed_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_closed(self):
        return self.status in {
            self.Status.CLOSED,
            self.Status.WITHDRAWN,
            self.Status.UNRESOLVED,
            self.Status.REJECTED,
        }

    @property
    def display_status(self):
        return self.get_status_display()


class DisputeParty(models.Model):
    """Multiple parties to a dispute - claimant or respondent."""

    class PartyRole(models.TextChoices):
        CLAIMANT = "claimant", "Claimant"
        RESPONDENT = "respondent", "Respondent"
        CO_CLAIMANT = "co_claimant", "Co-Claimant"
        CO_RESPONDENT = "co_respondent", "Co-Respondent"
        THIRD_PARTY = "third_party", "Third Party"

    class InvitationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        EXPIRED = "expired", "Expired"

    dispute = models.ForeignKey(
        Dispute, on_delete=models.CASCADE, related_name="parties"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dispute_participations",
    )
    role = models.CharField(max_length=20, choices=PartyRole.choices)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    representing_lawyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="party_representations",
    )
    joined_at = models.DateTimeField(null=True, blank=True)
    invitation_status = models.CharField(
        max_length=20,
        choices=InvitationStatus.choices,
        default=InvitationStatus.PENDING,
    )
    invitation_token = models.CharField(max_length=100, default=uuid.uuid4)
    position_statement = models.TextField(blank=True)
    requested_resolution = models.TextField(blank=True)
    has_accepted_jurisdiction = models.BooleanField(default=False)
    has_signed_confidentiality = models.BooleanField(default=False)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)

    class Meta:
        unique_together = [("dispute", "user")]
        ordering = ["id"]

    def __str__(self):
        return f"{self.user.email} as {self.get_role_display()} in {self.dispute.case_ref}"


class DisputeTimelineEntry(models.Model):
    """Case timeline / activity history (Section 4)."""

    class EntryType(models.TextChoices):
        CREATED = "created", "Case Created"
        SUBMITTED = "submitted", "Case Submitted"
        STATUS_CHANGE = "status_change", "Status Change"
        PARTY_INVITED = "party_invited", "Party Invited"
        PARTY_ACCEPTED = "party_accepted", "Party Accepted"
        PARTY_REJECTED = "party_rejected", "Party Rejected"
        DOCUMENT_UPLOADED = "document_uploaded", "Document Uploaded"
        MESSAGE_SENT = "message_sent", "Message Sent"
        PROPOSAL_MADE = "proposal_made", "Settlement Proposal Made"
        PROPOSAL_ACCEPTED = "proposal_accepted", "Proposal Accepted"
        PROPOSAL_REJECTED = "proposal_rejected", "Proposal Rejected"
        MEDIATOR_ASSIGNED = "mediator_assigned", "Mediator Assigned"
        SESSION_SCHEDULED = "session_scheduled", "Mediation Session Scheduled"
        SESSION_COMPLETED = "session_completed", "Session Completed"
        PAYMENT_MADE = "payment_made", "Payment Made"
        COMPLIANCE_UPDATE = "compliance_update", "Compliance Update"
        DEADLINE_REMINDER = "deadline_reminder", "Deadline Reminder"
        ADMIN_NOTE = "admin_note", "Admin Note"
        CLOSURE = "closure", "Case Closure"
        REOPEN = "reopen", "Case Reopened"
        OTHER = "other", "Other"

    dispute = models.ForeignKey(
        Dispute, on_delete=models.CASCADE, related_name="timeline_entries"
    )
    entry_type = models.CharField(max_length=30, choices=EntryType.choices)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dispute_timeline_actions",
    )
    metadata_json = models.JSONField(default=dict, blank=True)
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Dispute Timeline Entry"
        verbose_name_plural = "Dispute Timeline Entries"

    def __str__(self):
        return f"{self.dispute.case_ref} - {self.title}"
