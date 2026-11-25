"""Settlements app - Settlement records & agreements (Section 11 & 12)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class SettlementRecord(models.Model):
    """Generated settlement document (Section 12).

    Platform distinguishes between informal settlement record and
    mediated settlement agreement that satisfies statutory requirements.
    """

    class SettlementType(models.TextChoices):
        INFORMAL = "informal", "Informal Settlement Record"
        MEDIATED_AGREEMENT = "mediated_agreement", "Mediated Settlement Agreement"
        ENFORCEABLE_AGREEMENT = "enforceable_agreement", "Enforceable Settlement Agreement"
        PARTIAL = "partial", "Partial Settlement Record"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT_FOR_SIGNATURE = "sent_for_signature", "Sent for Signature"
        SIGNED_BY_SOME = "signed_by_some", "Partially Signed"
        FULLY_SIGNED = "fully_signed", "Fully Signed"
        EXECUTED = "executed", "Executed"
        SUPERSEDED = "superseded", "Superseded"
        TERMINATED = "terminated", "Terminated"

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="settlement_records"
    )
    case_ref_version = models.CharField(max_length=40, blank=True)
    settlement_type = models.CharField(
        max_length=30, choices=SettlementType.choices, default=SettlementType.INFORMAL
    )
    title = models.CharField(max_length=255)
    summary = models.TextField()
    terms = models.JSONField(default=list)
    payment_amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True
    )
    payment_schedule = models.JSONField(default=list, blank=True)
    obligations = models.JSONField(default=list, blank=True)
    conditions = models.JSONField(default=list, blank=True)
    compliance_deadlines = models.JSONField(default=list, blank=True)
    accepted_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="accepted_settlements", blank=True
    )
    signed_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="signed_settlements", blank=True
    )
    witness_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="witnessed_settlements", blank=True
    )
    mediator = models.ForeignKey(
        "mediators.MediatorProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="facilitated_settlements",
    )
    status = models.CharField(
        max_length=30, choices=Status.choices, default=Status.DRAFT
    )
    document_file = models.FileField(
        upload_to="settlement_docs/", null=True, blank=True, max_length=500
    )
    is_enforceable = models.BooleanField(default=False)
    legal_review_required = models.BooleanField(default=False)
    legal_reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by_lawyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="legally_reviewed_settlements",
    )
    created_at = models.DateTimeField(default=timezone.now)
    executed_at = models.DateTimeField(null=True, blank=True)
    version_number = models.PositiveIntegerField(default=1)
    parent_version = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="subsequent_versions"
    )
    is_current_version = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.dispute.case_ref}"


class SettlementSignature(models.Model):
    """Signature on a settlement record (Section 12)."""

    settlement = models.ForeignKey(
        SettlementRecord, on_delete=models.CASCADE, related_name="signatures"
    )
    signer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    signature_type = models.CharField(
        max_length=30,
        choices=[
            ("electronic", "Electronic Signature"),
            ("digital", "Digital Signature (PKI)"),
            ("witness", "Witness Signature"),
            ("mediator", "Mediator Counter-Signature"),
        ],
    )
    signed_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    signature_image = models.ImageField(upload_to="signatures/", null=True, blank=True)
    signature_hash = models.CharField(max_length=128, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)


class SettlementComplianceRecord(models.Model):
    """Track settlement obligations and payment milestones (Section 12)."""

    class ComplianceStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PARTIALLY_MET = "partially_met", "Partially Met"
        MET = "met", "Met"
        OVERDUE = "overdue", "Overdue"
        DEFAULTED = "defaulted", "Defaulted"
        WAIVED = "waived", "Waived"

    settlement = models.ForeignKey(
        SettlementRecord, on_delete=models.CASCADE, related_name="compliance_records"
    )
    obligation_description = models.TextField()
    responsible_party = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    due_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(
        max_length=20, choices=ComplianceStatus.choices, default=ComplianceStatus.PENDING
    )
    met_at = models.DateTimeField(null=True, blank=True)
    verification_proof = models.FileField(
        upload_to="compliance_proof/", null=True, blank=True
    )
    verification_notes = models.TextField(blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_compliance_records",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
