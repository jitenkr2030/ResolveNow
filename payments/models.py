"""Payments app - Payment and billing management (Section 13)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


def generate_payment_ref():
    return f"PAY-{uuid.uuid4().hex[:10].upper()}"


class Payment(models.Model):
    """Payment and billing records (Section 13)."""

    class PaymentType(models.TextChoices):
        REGISTRATION_FEE = "registration_fee", "Case Registration Fee"
        PLATFORM_FEE = "platform_fee", "Platform Service Charge"
        MEDIATOR_FEE = "mediator_fee", "Mediator Professional Fee"
        SUBSCRIPTION = "subscription", "Subscription Payment"
        REFUND = "refund", "Refund"
        PARTIAL_PAYMENT = "partial_payment", "Partial Payment"
        ADDITIONAL_CHARGE = "additional_charge", "Additional Charge"
        PENALTY = "penalty", "Late Payment Penalty"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        INITIATED = "initiated", "Initiated"
        SUCCESSFUL = "successful", "Successful"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"
        PARTIALLY_REFUNDED = "partially_refunded", "Partially Refunded"
        CANCELLED = "cancelled", "Cancelled"
        UNDER_REVIEW = "under_review", "Under Review"

    class PaymentGateway(models.TextChoices):
        RAZORPAY = "razorpay", "Razorpay"
        PAYU = "payu", "PayU"
        STRIPE = "stripe", "Stripe"
        UPI = "upi", "UPI"
        BANK_TRANSFER = "bank_transfer", "Bank Transfer"
        MANUAL = "manual", "Manual"
        OTHER = "other", "Other"

    payment_ref = models.CharField(
        max_length=40, unique=True, default=generate_payment_ref
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="payments"
    )
    dispute = models.ForeignKey(
        "disputes.Dispute",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    mediator = models.ForeignKey(
        "mediators.MediatorProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    payment_type = models.CharField(
        max_length=30, choices=PaymentType.choices, default=PaymentType.REGISTRATION_FEE
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # GST %
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.PENDING)
    payment_gateway = models.CharField(
        max_length=20, choices=PaymentGateway.choices, default=PaymentGateway.RAZORPAY
    )
    gateway_transaction_id = models.CharField(max_length=120, blank=True)
    gateway_order_id = models.CharField(max_length=120, blank=True)
    gateway_signature = models.CharField(max_length=255, blank=True)
    invoice_number = models.CharField(max_length=80, blank=True)
    invoice_path = models.FileField(
        upload_to="invoices/", null=True, blank=True, max_length=500
    )
    receipt_path = models.FileField(
        upload_to="receipts/", null=True, blank=True, max_length=500
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    initiated_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)
    refund_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    refund_date = models.DateTimeField(null=True, blank=True)
    refund_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["dispute"]),
            models.Index(fields=["payment_ref"]),
        ]

    def __str__(self):
        return f"{self.payment_ref} - {self.total_amount} {self.currency}"

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.amount + self.tax_amount
        super().save(*args, **kwargs)


class RefundRequest(models.Model):
    """Refund management (Section 13)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        PROCESSED = "processed", "Processed"
        CANCELLED = "cancelled", "Cancelled"

    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="refund_requests"
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    reason = models.TextField()
    requested_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="refund_requests_reviewed",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    admin_notes = models.TextField(blank=True)


class TaxInvoice(models.Model):
    """Tax invoice generation (Section 13)."""

    invoice_number = models.CharField(max_length=80, unique=True)
    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, related_name="invoice"
    )
    invoice_date = models.DateTimeField(default=timezone.now)
    bill_to_name = models.CharField(max_length=160)
    bill_to_address = models.TextField(blank=True)
    bill_to_gstin = models.CharField(max_length=20, blank=True)
    bill_to_pan = models.CharField(max_length=20, blank=True)
    line_items = models.JSONField(default=list)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cgst = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sgst = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    igst = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    file = models.FileField(upload_to="tax_invoices/", null=True, blank=True, max_length=500)


class SubscriptionPlan(models.Model):
    """Subscription plans (Section 13)."""

    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    monthly_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    annual_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    max_cases_per_month = models.PositiveIntegerField(null=True, blank=True)
    max_users = models.PositiveIntegerField(null=True, blank=True)
    api_access = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    features = models.JSONField(default=list, blank=True)
