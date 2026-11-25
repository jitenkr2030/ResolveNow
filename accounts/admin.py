"""Admin registration for the accounts app."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LoginHistory, AccountDeletionRequest


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_email_verified",
        "identity_verified",
        "is_active",
        "date_joined",
    )
    list_filter = ("role", "is_email_verified", "identity_verified", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone_number")
    ordering = ("-date_joined",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "alternate_phone",
                    "date_of_birth",
                    "address_line1",
                    "address_line2",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                    "preferred_language",
                    "timezone_preference",
                )
            },
        ),
        (
            "Role & verification",
            {
                "fields": (
                    "role",
                    "is_email_verified",
                    "is_mobile_verified",
                    "identity_verified",
                )
            },
        ),
        (
            "Security",
            {
                "fields": (
                    "mfa_enabled",
                    "is_suspended",
                    "suspension_reason",
                    "consent_terms_of_service",
                    "consent_privacy_policy",
                    "consent_marketing",
                    "consent_whatsapp",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "role", "password1", "password2"),
            },
        ),
    )


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "login_time", "ip_address", "device_type", "is_successful")
    list_filter = ("is_successful", "device_type")
    search_fields = ("user__email", "ip_address")
    readonly_fields = (
        "user",
        "login_time",
        "ip_address",
        "user_agent",
        "device_type",
        "browser",
        "os",
        "is_successful",
        "failure_reason",
        "session_key",
    )


@admin.register(AccountDeletionRequest)
class AccountDeletionRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "requested_at", "processed_at")
    list_filter = ("status",)
    search_fields = ("user__email",)
