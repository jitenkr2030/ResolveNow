"""Mediators app - Mediator registration and management (Section 7)."""
from django.db import models
from django.conf import settings
from django.utils import timezone


class MediatorProfile(models.Model):
    """Professional mediator profile (Section 7).

    Identity verification, qualifications, experience, certifications,
    practice areas, languages, fees, availability.
    """

    class ApprovalStatus(models.TextChoices):
        PENDING = "pending", "Pending Verification"
        UNDER_REVIEW = "under_review", "Under Review"
        APPROVED = "approved", "Approved"
        SUSPENDED = "suspended", "Suspended"
        REJECTED = "rejected", "Rejected"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mediator_profile"
    )
    professional_title = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    qualifications = models.JSONField(default=list, blank=True)
    certifications = models.JSONField(default=list, blank=True)
    practice_areas = models.JSONField(default=list, blank=True)
    specializations = models.JSONField(default=list, blank=True)
    languages_spoken = models.JSONField(default=list, blank=True)
    geographic_coverage = models.JSONField(default=list, blank=True)
    bar_council_registration = models.CharField(max_length=80, blank=True)
    mediator_registration_number = models.CharField(max_length=80, blank=True)
    hourly_fee = models.DecimalField(max_digits=12, decimal_places=2, default=2500)
    half_day_fee = models.DecimalField(max_digits=12, decimal_places=2, default=15000)
    full_day_fee = models.DecimalField(max_digits=12, decimal_places=2, default=25000)
    currency = models.CharField(max_length=10, default="INR")
    rating = models.DecimalField(
        max_digits=4, decimal_places=2, default=0
    )
    total_ratings = models.PositiveIntegerField(default=0)
    total_cases_handled = models.PositiveIntegerField(default=0)
    successful_settlements = models.PositiveIntegerField(default=0)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    approval_status = models.CharField(
        max_length=20, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mediator_approvals_done",
    )
    suspension_reason = models.TextField(blank=True)
    suspended_at = models.DateTimeField(null=True, blank=True)
    is_accepting_new_cases = models.BooleanField(default=True)
    profile_photo = models.ImageField(upload_to="mediator_photos/", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-rating", "-years_of_experience"]
        verbose_name = "Mediator Profile"
        verbose_name_plural = "Mediator Profiles"

    def __str__(self):
        return f"{self.user.full_name} ({self.user.email})"

    @property
    def is_verified(self):
        return self.approval_status == self.ApprovalStatus.APPROVED


class MediatorAvailability(models.Model):
    """Availability calendar for a mediator (Section 7 & 9)."""

    class DayOfWeek(models.TextChoices):
        MON = "monday", "Monday"
        TUE = "tuesday", "Tuesday"
        WED = "wednesday", "Wednesday"
        THU = "thursday", "Thursday"
        FRI = "friday", "Friday"
        SAT = "saturday", "Saturday"
        SUN = "sunday", "Sunday"

    mediator = models.ForeignKey(
        MediatorProfile, on_delete=models.CASCADE, related_name="availability_slots"
    )
    day_of_week = models.CharField(max_length=20, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    availability_timezone = models.CharField(max_length=50, default="Asia/Kolkata")
    is_recurring = models.BooleanField(default=True)
    specific_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)


class MediatorFeedback(models.Model):
    """Mediator feedback and ratings (Section 7 & 19)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PUBLISHED = "published", "Published"
        HIDDEN = "hidden", "Hidden"

    mediator = models.ForeignKey(
        MediatorProfile, on_delete=models.CASCADE, related_name="feedbacks"
    )
    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.SET_NULL, null=True, blank=True
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField()  # 1-5
    feedback_text = models.TextField()
    communication_rating = models.PositiveSmallIntegerField(default=0)
    impartiality_rating = models.PositiveSmallIntegerField(default=0)
    professionalism_rating = models.PositiveSmallIntegerField(default=0)
    timeliness_rating = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [("mediator", "dispute", "reviewer")]


class ConflictOfInterestDeclaration(models.Model):
    """Conflict-of-interest declaration per assignment (Section 8 & 20)."""

    mediator = models.ForeignKey(
        MediatorProfile, on_delete=models.CASCADE, related_name="coi_declarations"
    )
    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="coi_declarations"
    )
    has_conflict = models.BooleanField(default=False)
    declaration_text = models.TextField()
    declared_at = models.DateTimeField(default=timezone.now)
    is_accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)
    reviewed_by_admin = models.BooleanField(default=False)
