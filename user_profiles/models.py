"""User profiles app - Extended profile data and KYC references."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class UserProfile(models.Model):
    """Extended user profile data (Section 1)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile_extended",
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)
    occupation = models.CharField(max_length=120, blank=True)
    employer = models.CharField(max_length=160, blank=True)
    annual_income = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    pan_number = models.CharField(max_length=20, blank=True)  # Income-tax PAN
    aadhaar_last4 = models.CharField(max_length=4, blank=True)  # last 4 of Aadhaar
    gstin = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=[
            ("email", "Email"),
            ("sms", "SMS"),
            ("whatsapp", "WhatsApp"),
            ("call", "Phone call"),
        ],
        default="email",
    )
    profile_completion_pct = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"Profile of {self.user.email}"

    def calculate_completion(self):
        fields = [
            self.user.first_name,
            self.user.last_name,
            self.user.phone_number,
            self.user.address_line1,
            self.user.city,
            self.user.state,
            self.user.postal_code,
            self.occupation,
            self.pan_number,
            self.avatar,
        ]
        completed = sum(1 for f in fields if f)
        self.profile_completion_pct = int((completed / len(fields)) * 100)
        self.save(update_fields=["profile_completion_pct"])
        return self.profile_completion_pct


class OrganizationMembership(models.Model):
    """Link a user to an organization with a role."""

    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Administrator"
        MANAGER = "manager", "Manager"
        MEMBER = "member", "Member"
        VIEWER = "viewer", "Viewer"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="org_memberships"
    )
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="members"
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    designation = models.CharField(max_length=120, blank=True)
    department = models.CharField(max_length=120, blank=True)
    joined_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="org_invitations_sent",
    )

    class Meta:
        unique_together = [("user", "organization")]
        verbose_name = "Organization Membership"
        verbose_name_plural = "Organization Memberships"

    def __str__(self):
        return f"{self.user.email} @ {self.organization.name} ({self.role})"
