"""Negotiation app - Online negotiation workspace (Section 5)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class NegotiationRoom(models.Model):
    """Private negotiation room within a dispute (Section 5)."""

    dispute = models.OneToOneField(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="negotiation_room"
    )
    is_open = models.BooleanField(default=True)
    opened_at = models.DateTimeField(default=timezone.now)
    closed_at = models.DateTimeField(null=True, blank=True)
    negotiation_deadline = models.DateTimeField(null=True, blank=True)
    is_mediator_assisted = models.BooleanField(default=False)

    def __str__(self):
        return f"Negotiation room for {self.dispute.case_ref}"


class SettlementProposal(models.Model):
    """Settlement proposal in negotiation (Section 5 & 11)."""

    class ProposalType(models.TextChoices):
        INITIAL_OFFER = "initial_offer", "Initial Settlement Offer"
        COUNTER_OFFER = "counter_offer", "Counteroffer"
        REVISED_PROPOSAL = "revised_proposal", "Revised Settlement Proposal"
        MEDIATOR_PROPOSAL = "mediator_proposal", "Mediator-Proposed Settlement"
        FINAL_OFFER = "final_offer", "Final Offer"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        COUNTERED = "countered", "Countered"
        EXPIRED = "expired", "Expired"
        WITHDRAWN = "withdrawn", "Withdrawn"
        PARTIALLY_ACCEPTED = "partially_accepted", "Partially Accepted"

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="settlement_proposals"
    )
    room = models.ForeignKey(
        NegotiationRoom, on_delete=models.CASCADE, null=True, blank=True,
        related_name="proposals"
    )
    proposal_type = models.CharField(
        max_length=30, choices=ProposalType.choices, default=ProposalType.INITIAL_OFFER
    )
    proposed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="settlement_proposals_made",
    )
    proposed_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="settlement_proposals_received", blank=True
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    payment_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True
    )
    payment_due_date = models.DateField(null=True, blank=True)
    is_instalment = models.BooleanField(default=False)
    instalment_count = models.PositiveIntegerField(default=1)
    instalment_schedule = models.JSONField(default=dict, blank=True)
    obligations = models.JSONField(default=list, blank=True)
    conditions = models.JSONField(default=list, blank=True)
    attached_documents = models.ManyToManyField(
        "documents.Document", related_name="proposals_using", blank=True
    )
    parent_proposal = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="counters"
    )
    status = models.CharField(
        max_length=25, choices=Status.choices, default=Status.DRAFT
    )
    valid_until = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.dispute.case_ref}"


class ProposalResponse(models.Model):
    """Acceptance / rejection / counter of a proposal (Section 5)."""

    class Response(models.TextChoices):
        ACCEPT = "accept", "Accept"
        REJECT = "reject", "Reject"
        COUNTER = "counter", "Counter"
        REQUEST_MODIFICATION = "request_modification", "Request Modification"

    proposal = models.ForeignKey(
        SettlementProposal, on_delete=models.CASCADE, related_name="responses"
    )
    responder = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    response = models.CharField(max_length=30, choices=Response.choices)
    message = models.TextField(blank=True)
    counter_proposal = models.ForeignKey(
        SettlementProposal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="response_link",
    )
    responded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-responded_at"]


class NegotiationActivity(models.Model):
    """Negotiation activity tracking (Section 5)."""

    class ActivityType(models.TextChoices):
        ROOM_OPENED = "room_opened", "Negotiation Room Opened"
        PROPOSAL_DRAFTED = "proposal_drafted", "Proposal Drafted"
        PROPOSAL_SUBMITTED = "proposal_submitted", "Proposal Submitted"
        PROPOSAL_ACCEPTED = "proposal_accepted", "Proposal Accepted"
        PROPOSAL_REJECTED = "proposal_rejected", "Proposal Rejected"
        PROPOSAL_COUNTERED = "proposal_countered", "Proposal Countered"
        INVITATION_SENT = "invitation_sent", "Negotiation Invitation Sent"
        DEADLINE_EXTENDED = "deadline_extended", "Deadline Extended"
        ROOM_CLOSED = "room_closed", "Negotiation Room Closed"

    room = models.ForeignKey(
        NegotiationRoom, on_delete=models.CASCADE, related_name="activities"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="negotiation_activities",
    )
    activity_type = models.CharField(max_length=30, choices=ActivityType.choices)
    description = models.TextField(blank=True)
    related_proposal = models.ForeignKey(
        SettlementProposal, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
