"""Verification app - Identity verification (KYC), email/mobile verification."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class VerificationRecord(models.Model):
    """KYC / identity verification record (Section 1 & 20)."""

    class VerificationType(models.TextChoices):
        EMAIL = "email", "Email"
        MOBILE = "mobile", "Mobile"
        AADHAAR = "aadhaar", "Aadhaar"
        PAN = "pan", "PAN Card"
        PASSPORT = "passport", "Passport"
        DRIVING_LICENSE = "driving_license", "Driving License"
        VOTER_ID = "voter_id", "Voter ID"
        BUSINESS_REG = "business_registration", "Business Registration"
        GST = "gst", "GST Certificate"
        BAR_COUNCIL = "bar_council", "Bar Council Registration"
        MEDIATOR_CERT = "mediator_certification", "Mediator Certification"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        UNDER_REVIEW = "under_review", "Under Review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        EXPIRED = "expired", "Expired"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification_records",
    )
    verification_type = models.CharField(
        max_length=30, choices=VerificationType.choices
    )
    document = models.FileField(upload_to="verification_docs/", null=True, blank=True)
    document_number = models.CharField(max_length=80, blank=True)  # masked
    document_number_hash = models.CharField(max_length=128, blank=True)
    issuing_authority = models.CharField(max_length=160, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    submitted_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verifications_reviewed",
    )
    reviewer_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    verification_token = models.CharField(
        max_length=100, default=str(uuid.uuid4), unique=True
    )

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Verification Record"
        verbose_name_plural = "Verification Records"

    def __str__(self):
        return f"{self.user.email} - {self.get_verification_type_display()} ({self.status})"


class OTPVerification(models.Model):
    """Email/mobile OTP verification (Section 1)."""

    class Channel(models.TextChoices):
        EMAIL = "email", "Email"
        SMS = "sms", "SMS"
        WHATSAPP = "whatsapp", "WhatsApp"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otp_verifications",
    )
    channel = models.CharField(max_length=20, choices=Channel.choices)
    target = models.CharField(max_length=120)  # email or phone
    otp_code = models.CharField(max_length=8)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def is_valid(self, code):
        return (
            not self.is_used
            and self.expires_at > timezone.now()
            and self.attempts < 5
            and self.otp_code == code
        )
