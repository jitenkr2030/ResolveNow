"""Dispute categories app (Section 3)."""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class DisputeCategory(models.Model):
    """Dispute category - Section 3.

    Supported categories: Commercial, Financial, Employment, Consumer,
    Property, Partnership, Family, Housing, Education, Vendor, Technology, Insurance.
    """

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    examples = models.TextField(blank=True, help_text="Comma-separated examples.")
    is_active = models.BooleanField(default=True)
    minimum_disputed_amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=1000
    )
    maximum_disputed_amount = models.DecimalField(
        max_digits=16, decimal_places=2, default=50000000
    )
    default_priority = models.CharField(
        max_length=20,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium",
    )
    requires_legal_suitability_check = models.BooleanField(default=True)
    requires_kyc = models.BooleanField(default=False)
    estimated_resolution_days = models.PositiveIntegerField(default=45)
    icon_class = models.CharField(max_length=80, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Dispute Category"
        verbose_name_plural = "Dispute Categories"

    def __str__(self):
        return self.name

    @classmethod
    def default_categories_data(cls):
        return [
            ("Commercial", "Business and contractual disputes"),
            ("Financial", "Outstanding payments and invoices"),
            ("Employment", "Workplace and employment disputes"),
            ("Consumer", "Product and service complaints"),
            ("Property", "Rental and property-related disputes"),
            ("Partnership", "Business partnership disagreements"),
            ("Family", "Suitable family and personal disputes"),
            ("Housing", "Resident and housing society disputes"),
            ("Education", "Institutional fee and service disputes"),
            ("Vendor", "Supplier and customer disagreements"),
            ("Technology", "IT service and software contracts"),
            ("Insurance", "Suitable insurance-related disputes"),
        ]


class LegalEligibilityChecklist(models.Model):
    """Eligibility / suitability screening questions per category."""

    category = models.ForeignKey(
        DisputeCategory, on_delete=models.CASCADE, related_name="eligibility_questions"
    )
    question = models.TextField()
    help_text = models.TextField(blank=True)
    is_required = models.BooleanField(default=True)
    disqualifying_if_yes = models.BooleanField(
        default=False,
        help_text="If the answer is 'Yes', the dispute is not eligible for ODR.",
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.category.name} - Q{self.display_order}"


class DisputeEligibilityResult(models.Model):
    """Saved eligibility screening result for a dispute."""

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="eligibility_results"
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="dispute_eligibility_reviews",
    )
    is_eligible = models.BooleanField(default=False)
    eligibility_score = models.PositiveIntegerField(default=0)  # 0-100
    notes = models.TextField(blank=True)
    disqualifying_reasons = models.TextField(blank=True)
    requires_human_review = models.BooleanField(default=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    decision = models.CharField(
        max_length=20,
        choices=[
            ("eligible", "Eligible for Mediation"),
            ("conditional", "Conditionally Eligible"),
            ("ineligible", "Ineligible - Recommend Litigation"),
            ("pending", "Awaiting Review"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.dispute.case_ref} - {self.decision}"
