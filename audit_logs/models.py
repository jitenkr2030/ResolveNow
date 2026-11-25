"""Audit logs app (Section 20)."""
from django.db import models
from django.conf import settings
from django.utils import timezone


class AuditLog(models.Model):
    """Activity audit trails (Section 20).

    Captured via AuditLogMiddleware for every request, plus explicit audit
    events for sensitive actions.
    """

    class Action(models.TextChoices):
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        FAILED_LOGIN = "failed_login", "Failed Login"
        CREATE = "create", "Create"
        UPDATE = "update", "Update"
        DELETE = "delete", "Delete"
        VIEW = "view", "View"
        DOWNLOAD = "download", "Download"
        UPLOAD = "upload", "Upload"
        PERMISSION_CHANGE = "permission_change", "Permission Change"
        CONFIG_CHANGE = "config_change", "Configuration Change"
        EXPORT = "export", "Data Export"
        OTHER = "other", "Other"

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=30, choices=Action.choices)
    resource_type = models.CharField(max_length=80, blank=True)
    resource_id = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    metadata_json = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    request_path = models.CharField(max_length=255, blank=True)
    request_method = models.CharField(max_length=10, blank=True)
    status_code = models.PositiveIntegerField(null=True, blank=True)
    session_key = models.CharField(max_length=80, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        indexes = [
            models.Index(fields=["actor"]),
            models.Index(fields=["action"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"{self.actor} - {self.action} @ {self.timestamp:%Y-%m-%d %H:%M}"


class SystemConfigurationLog(models.Model):
    """Configuration change log."""

    config_key = models.CharField(max_length=120)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    changed_at = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=255, blank=True)
