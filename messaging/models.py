"""Messaging app - Secure in-platform messaging (Section 5 & 14)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class MessageThread(models.Model):
    """Secure messaging thread scoped to a dispute (Section 5 & 14)."""

    class ThreadType(models.TextChoices):
        PARTY_TO_PARTY = "party_to_party", "Party-to-Party"
        MEDIATOR_LED = "mediator_led", "Mediator-Led Discussion"
        CAUCUS_PRIVATE = "caucus_private", "Private Caucus"
        ADMIN_INTERNAL = "admin_internal", "Administrators Only"
        GENERAL = "general", "General Discussion"

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="message_threads"
    )
    title = models.CharField(max_length=200, default="Discussion")
    thread_type = models.CharField(
        max_length=20, choices=ThreadType.choices, default=ThreadType.GENERAL
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="message_threads"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_threads",
    )
    is_locked = models.BooleanField(default=False)
    last_message_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-last_message_at"]

    def __str__(self):
        return f"{self.title} - {self.dispute.case_ref}"


class Message(models.Model):
    """A single secure message in a thread (Section 5)."""

    thread = models.ForeignKey(
        MessageThread, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    body = models.TextField()
    attachments = models.ManyToManyField(
        "documents.Document", related_name="attached_to_messages", blank=True
    )
    is_read_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="read_messages", blank=True
    )
    is_moderator_message = models.BooleanField(default=False)
    is_system_message = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["sent_at"]

    def __str__(self):
        return f"Message from {self.sender.email} @ {self.sent_at:%Y-%m-%d %H:%M}"


class Notification(models.Model):
    """Cross-platform notifications (Section 14).

    In-platform, email, SMS, WhatsApp.
    """

    class Channel(models.TextChoices):
        IN_PLATFORM = "in_platform", "In-Platform"
        EMAIL = "email", "Email"
        SMS = "sms", "SMS"
        WHATSAPP = "whatsapp", "WhatsApp"
        PUSH = "push", "Push"

    class NotificationType(models.TextChoices):
        CASE_REGISTRATION = "case_registration", "Case Registration"
        DOCUMENT_SUBMISSION = "document_submission", "Document Submitted"
        MEDIATOR_ASSIGNMENT = "mediator_assignment", "Mediator Assigned"
        MEETING_REMINDER = "meeting_reminder", "Meeting Reminder"
        SETTLEMENT_PROPOSAL = "settlement_proposal", "Settlement Proposal"
        PAYMENT = "payment", "Payment Notification"
        DEADLINE_REMINDER = "deadline_reminder", "Deadline Reminder"
        CASE_STATUS_UPDATE = "case_status_update", "Case Status Update"
        ADMIN_ANNOUNCEMENT = "admin_announcement", "Administrative Announcement"
        MESSAGE_RECEIVED = "message_received", "Message Received"
        PARTY_INVITATION = "party_invitation", "Party Invitation"
        VERIFICATION = "verification", "Verification Update"
        OTHER = "other", "Other"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notification_type = models.CharField(
        max_length=30, choices=NotificationType.choices
    )
    channel = models.CharField(
        max_length=20, choices=Channel.choices, default=Channel.IN_PLATFORM
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    dispute = models.ForeignKey(
        "disputes.Dispute",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )
    related_url = models.CharField(max_length=255, blank=True)
    is_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["recipient", "is_read"])]

    def __str__(self):
        return f"{self.subject} -> {self.recipient.email}"


class NotificationPreference(models.Model):
    """User notification preferences (Section 14)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification_prefs"
    )
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    whatsapp_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)
    case_registration = models.BooleanField(default=True)
    document_submission = models.BooleanField(default=True)
    mediator_assignment = models.BooleanField(default=True)
    meeting_reminder = models.BooleanField(default=True)
    settlement_proposal = models.BooleanField(default=True)
    payment = models.BooleanField(default=True)
    deadline_reminder = models.BooleanField(default=True)
    case_status_update = models.BooleanField(default=True)
    admin_announcement = models.BooleanField(default=True)
    message_received = models.BooleanField(default=True)
    digest_frequency = models.CharField(
        max_length=20,
        choices=[
            ("instant", "Instant"),
            ("hourly", "Hourly"),
            ("daily", "Daily"),
            ("weekly", "Weekly"),
        ],
        default="instant",
    )
