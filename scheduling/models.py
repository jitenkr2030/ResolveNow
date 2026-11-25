"""Scheduling app - Mediation scheduling and calendar (Section 9)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class ScheduledSession(models.Model):
    """Mediation session scheduling (Section 9)."""

    class SessionType(models.TextChoices):
        JOINT = "joint", "Joint Mediation Session"
        CAUCUS = "caucus", "Private Caucus"
        PRELIMINARY = "preliminary", "Preliminary Session"
        FOLLOW_UP = "follow_up", "Follow-Up Session"
        SETTLEMENT_DRAFTING = "settlement_drafting", "Settlement Drafting Session"

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        RESCHEDULE_REQUESTED = "reschedule_requested", "Reschedule Requested"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"
        NO_SHOW = "no_show", "No-Show"
        IN_PROGRESS = "in_progress", "In Progress"

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="scheduled_sessions"
    )
    mediator = models.ForeignKey(
        "mediators.MediatorProfile", on_delete=models.CASCADE, related_name="scheduled_sessions"
    )
    session_type = models.CharField(
        max_length=30, choices=SessionType.choices, default=SessionType.JOINT
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    session_timezone = models.CharField(max_length=50, default="Asia/Kolkata")
    duration_minutes = models.PositiveIntegerField(default=90)
    status = models.CharField(
        max_length=30, choices=Status.choices, default=Status.SCHEDULED
    )
    scheduled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="sessions_scheduled",
    )
    is_online = models.BooleanField(default=True)
    meeting_link = models.CharField(max_length=255, blank=True)
    meeting_id = models.CharField(max_length=80, blank=True)
    meeting_password = models.CharField(max_length=80, blank=True)
    external_calendar_event_id = models.CharField(max_length=160, blank=True)
    reminder_sent = models.BooleanField(default=False)
    completion_summary = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["scheduled_start"]
        verbose_name = "Scheduled Session"
        verbose_name_plural = "Scheduled Sessions"

    def __str__(self):
        return f"{self.title} - {self.scheduled_start:%Y-%m-%d %H:%M}"


class SessionParticipant(models.Model):
    """Participant attendance records (Section 9)."""

    class Attendance(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmed"
        TENTATIVE = "tentative", "Tentative"
        DECLINED = "declined", "Declined"
        PENDING = "pending", "Pending"
        ATTENDED = "attended", "Attended"
        ABSENT = "absent", "Absent"

    session = models.ForeignKey(
        ScheduledSession, on_delete=models.CASCADE, related_name="participants"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    role_in_session = models.CharField(max_length=40, blank=True)
    attendance_status = models.CharField(
        max_length=20, choices=Attendance.choices, default=Attendance.PENDING
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    joined_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)


class RescheduleRequest(models.Model):
    """Reschedule / cancellation request (Section 9)."""

    class Type(models.TextChoices):
        RESCHEDULE = "reschedule", "Reschedule"
        CANCEL = "cancel", "Cancel"

    session = models.ForeignKey(
        ScheduledSession, on_delete=models.CASCADE, related_name="reschedule_requests"
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    request_type = models.CharField(max_length=20, choices=Type.choices)
    proposed_start = models.DateTimeField(null=True, blank=True)
    proposed_end = models.DateTimeField(null=True, blank=True)
    reason = models.TextField()
    requested_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reschedule_approvals",
    )
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-requested_at"]
