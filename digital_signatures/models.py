"""Digital signatures app - Electronic signing (Section 21)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
import hashlib


class DigitalSignature(models.Model):
    """Digital signature with identity verification, timestamps,
    document integrity verification (Section 21 - Digital Agreement Execution).
    """

    class SignatureMethod(models.TextChoices):
        TYPED = "typed", "Typed Signature"
        UPLOADED_IMAGE = "uploaded_image", "Uploaded Signature Image"
        DRAWN = "drawn", "Drawn Signature"
        AADHAAR_ESIGN = "aadhaar_esign", "Aadhaar e-Sign"
        USB_TOKEN = "usb_token", "USB Token (PKI)"
        EMUDRA = "emudra", "eMudra"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REQUESTED = "requested", "Signature Requested"
        SIGNED = "signed", "Signed"
        DECLINED = "declined", "Declined"
        EXPIRED = "expired", "Expired"
        REVOKED = "revoked", "Revoked"

    document = models.ForeignKey(
        "documents.Document", on_delete=models.CASCADE, related_name="digital_signatures"
    )
    signer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="signatures"
    )
    signature_method = models.CharField(
        max_length=20, choices=SignatureMethod.choices, default=SignatureMethod.TYPED
    )
    signature_image = models.ImageField(upload_to="digital_signatures/", null=True, blank=True)
    signature_data = models.TextField(blank=True)  # base64 of drawn signature
    signature_hash = models.CharField(max_length=128, blank=True)
    document_hash_at_signing = models.CharField(max_length=128, blank=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    requested_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    geolocation = models.CharField(max_length=120, blank=True)
    aadhaar_last4 = models.CharField(max_length=4, blank=True)
    verification_token = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    audit_reference = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["-requested_at"]
        verbose_name = "Digital Signature"
        verbose_name_plural = "Digital Signatures"

    def generate_hashes(self):
        if self.document and self.document.file:
            self.document.file.open("rb")
            data = self.document.file.read()
            self.document_hash_at_signing = hashlib.sha256(data).hexdigest()
            self.document.file.close()
        if self.signature_data:
            self.signature_hash = hashlib.sha256(self.signature_data.encode()).hexdigest()
