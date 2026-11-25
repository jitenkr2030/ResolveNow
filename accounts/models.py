"""
Accounts app - Custom User model with role-based permissions.

Implements Section 1 (User Registration & Account Management) and Section 22 (User Roles).
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    """Custom manager for the User model using email as the unique identifier."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "super_admin")
        extra_fields.setdefault("is_email_verified", True)
        extra_fields.setdefault("is_mobile_verified", True)
        extra_fields.setdefault("identity_verified", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model.

    Implements role-based access (Section 22):
    individual, claimant, respondent, business, lawyer, mediator,
    case_manager, finance_manager, grievance_officer, administrator, super_admin.
    """

    class Role(models.TextChoices):
        INDIVIDUAL = "individual", _("Individual")
        CLAIMANT = "claimant", _("Claimant")
        RESPONDENT = "respondent", _("Respondent")
        BUSINESS = "business", _("Business User")
        LAWYER = "lawyer", _("Lawyer")
        MEDIATOR = "mediator", _("Mediator")
        CASE_MANAGER = "case_manager", _("Case Manager")
        FINANCE_MANAGER = "finance_manager", _("Finance Manager")
        GRIEVANCE_OFFICER = "grievance_officer", _("Grievance Officer")
        ADMINISTRATOR = "administrator", _("Administrator")
        SUPER_ADMIN = "super_admin", _("Super Admin")

    username = None  # remove username; use email
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(
        _("role"), max_length=30, choices=Role.choices, default=Role.INDIVIDUAL
    )

    # Profile fields
    first_name = models.CharField(_("first name"), max_length=80)
    last_name = models.CharField(_("last name"), max_length=80)
    phone_number = models.CharField(_("mobile number"), max_length=20, blank=True)
    alternate_phone = models.CharField(_("alternate phone"), max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address_line1 = models.CharField(_("address line 1"), max_length=255, blank=True)
    address_line2 = models.CharField(_("address line 2"), max_length=255, blank=True)
    city = models.CharField(_("city"), max_length=80, blank=True)
    state = models.CharField(_("state"), max_length=80, blank=True)
    postal_code = models.CharField(_("postal code"), max_length=20, blank=True)
    country = models.CharField(_("country"), max_length=60, default="India")
    preferred_language = models.CharField(
        _("preferred language"), max_length=30, default="English"
    )
    timezone_preference = models.CharField(
        _("timezone"), max_length=50, default="Asia/Kolkata"
    )

    # Verification status
    is_email_verified = models.BooleanField(_("email verified"), default=False)
    is_mobile_verified = models.BooleanField(_("mobile verified"), default=False)
    identity_verified = models.BooleanField(_("identity verified (KYC)"), default=False)
    email_verification_token = models.CharField(
        max_length=100, blank=True, default=str(uuid.uuid4)
    )

    # Security
    mfa_enabled = models.BooleanField(_("multi-factor authentication"), default=False)
    mfa_secret = models.CharField(_("MFA secret"), max_length=64, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    is_suspended = models.BooleanField(_("account suspended"), default=False)
    suspension_reason = models.TextField(blank=True)
    suspension_date = models.DateTimeField(null=True, blank=True)

    # Consent
    consent_terms_of_service = models.BooleanField(default=False)
    consent_privacy_policy = models.BooleanField(default=False)
    consent_marketing = models.BooleanField(default=False)
    consent_whatsapp = models.BooleanField(default=False)
    consent_timestamp = models.DateTimeField(null=True, blank=True)

    # Timestamps
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.first_name

    @property
    def is_mediator(self):
        return self.role == self.Role.MEDIATOR

    @property
    def is_lawyer(self):
        return self.role == self.Role.LAWYER

    @property
    def is_business_user(self):
        return self.role == self.Role.BUSINESS

    @property
    def is_staff_member(self):
        return self.role in {
            self.Role.CASE_MANAGER,
            self.Role.FINANCE_MANAGER,
            self.Role.GRIEVANCE_OFFICER,
            self.Role.ADMINISTRATOR,
            self.Role.SUPER_ADMIN,
            self.Role.MEDIATOR,
        }

    @property
    def is_admin_level(self):
        return self.role in {
            self.Role.ADMINISTRATOR,
            self.Role.SUPER_ADMIN,
        }

    @property
    def display_role(self):
        return self.get_role_display()


class LoginHistory(models.Model):
    """Tracks login history and device management (Section 1)."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="login_history"
    )
    login_time = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=30, blank=True)  # mobile/tablet/desktop
    browser = models.CharField(max_length=80, blank=True)
    os = models.CharField(max_length=80, blank=True)
    location = models.CharField(max_length=120, blank=True)
    is_successful = models.BooleanField(default=True)
    failure_reason = models.CharField(max_length=255, blank=True)
    session_key = models.CharField(max_length=80, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-login_time"]
        verbose_name = "Login History"
        verbose_name_plural = "Login History"

    def __str__(self):
        return f"{self.user.email} @ {self.login_time:%Y-%m-%d %H:%M}"


class AccountDeletionRequest(models.Model):
    """Account suspension and deletion requests (Section 1)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="deletion_requests"
    )
    reason = models.TextField()
    requested_at = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_deletion_requests",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return f"Deletion request by {self.user.email} ({self.status})"
