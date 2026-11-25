"""Organizations app - Business & corporate accounts (Section 17)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Organization(models.Model):
    """Business / corporate / institutional account (Section 1 & 17)."""

    class OrgType(models.TextChoices):
        SOLE_PROPRIETOR = "sole_proprietor", "Sole Proprietor"
        PARTNERSHIP = "partnership", "Partnership"
        LLP = "llp", "Limited Liability Partnership"
        PRIVATE_LIMITED = "private_limited", "Private Limited Company"
        PUBLIC_LIMITED = "public_limited", "Public Limited Company"
        MSME = "msme", "MSME / Small Business"
        NGO = "ngo", "Non-Governmental Organization"
        GOVERNMENT = "government", "Government Body"
        INSTITUTION = "institution", "Educational Institution"
        OTHER = "other", "Other"

    class VerificationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        UNDER_REVIEW = "under_review", "Under Review"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"

    name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=240, blank=True)
    org_type = models.CharField(max_length=30, choices=OrgType.choices)
    registration_number = models.CharField(max_length=60, blank=True)
    gstin = models.CharField(max_length=20, blank=True)
    pan = models.CharField(max_length=20, blank=True)
    tan = models.CharField(max_length=20, blank=True)
    cin = models.CharField(max_length=24, blank=True)
    industry = models.CharField(max_length=120, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    employee_count = models.PositiveIntegerField(null=True, blank=True)
    annual_revenue = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True
    )

    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=80, blank=True)
    state = models.CharField(max_length=80, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=60, default="India")

    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="org_logos/", null=True, blank=True)

    primary_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_organizations",
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )
    verification_notes = models.TextField(blank=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="org_verifications_done",
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name

    @property
    def is_verified(self):
        return self.verification_status == self.VerificationStatus.VERIFIED


class Subscription(models.Model):
    """Organization subscription plan."""

    class Plan(models.TextChoices):
        FREE = "free", "Free"
        STARTER = "starter", "Starter"
        BUSINESS = "business", "Business"
        ENTERPRISE = "enterprise", "Enterprise"
        CUSTOM = "custom", "Custom"

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.CharField(max_length=20, choices=Plan.choices, default=Plan.FREE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    monthly_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    max_cases_per_month = models.PositiveIntegerField(null=True, blank=True)
    max_users = models.PositiveIntegerField(null=True, blank=True)
    api_access = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.organization.name} - {self.get_plan_display()}"
