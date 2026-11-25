"""Mediation sessions app - Online mediation room (Section 10)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class MediationRoom(models.Model):
    """Online mediation room (Section 10).

    Recording is disabled by default and only enabled where lawful with consent.
    """

    session = models.OneToOneField(
        "scheduling.ScheduledSession", on_delete=models.CASCADE, related_name="room"
    )
    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="mediation_rooms"
    )
    mediator = models.ForeignKey(
        "mediators.MediatorProfile", on_delete=models.SET_NULL, null=True,
        related_name="mediation_rooms",
    )
    room_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    room_url = models.CharField(max_length=255, blank=True)
    access_password = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    enable_recording = models.BooleanField(default=False)
    recording_consent_obtained = models.BooleanField(default=False)
    recording_started_at = models.DateTimeField(null=True, blank=True)
    recording_url = models.CharField(max_length=255, blank=True)
    waiting_room_enabled = models.BooleanField(default=True)
    allow_screen_sharing = models.BooleanField(default=True)
    allow_document_presentation = models.BooleanField(default=True)
    allow_private_caucus = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]


class RoomParticipant(models.Model):
    """Participant in a mediation room (Section 10)."""

    class Role(models.TextChoices):
        MEDIATOR = "mediator", "Mediator / Host"
        CLAIMANT = "claimant", "Claimant"
        RESPONDENT = "respondent", "Respondent"
        LAWYER = "lawyer", "Lawyer"
        OBSERVER = "observer", "Observer"
        ADMIN = "admin", "Administrator"

    class Status(models.TextChoices):
        INVITED = "invited", "Invited"
        IN_WAITING_ROOM = "in_waiting_room", "In Waiting Room"
        ADMITTED = "admitted", "Admitted"
        IN_SESSION = "in_session", "In Session"
        LEFT = "left", "Left"
        REMOVED = "removed", "Removed"

    room = models.ForeignKey(
        MediationRoom, on_delete=models.CASCADE, related_name="participants"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.INVITED)
    joined_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)
    has_audio = models.BooleanField(default=False)
    has_video = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    is_video_off = models.BooleanField(default=False)
    is_screen_sharing = models.BooleanField(default=False)
    consent_to_recording = models.BooleanField(default=False)


class SessionNote(models.Model):
    """Session notes / mediator session summary (Section 10)."""

    class NoteType(models.TextChoices):
        PRIVATE = "private", "Private Note"
        SHARED = "shared", "Shared with Parties"
        SESSION_SUMMARY = "session_summary", "Session Summary"
        CAUCUS = "caucus", "Private Caucus Note"

    room = models.ForeignKey(
        MediationRoom, on_delete=models.CASCADE, related_name="session_notes"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    note_type = models.CharField(
        max_length=20, choices=NoteType.choices, default=NoteType.PRIVATE
    )
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_visible_to_parties = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class PrivateCaucus(models.Model):
    """Separate party sessions / private caucus rooms (Section 10)."""

    room = models.ForeignKey(
        MediationRoom, on_delete=models.CASCADE, related_name="private_caucuses"
    )
    party_side = models.CharField(
        max_length=20,
        choices=[("claimant", "Claimant Side"), ("respondent", "Respondent Side")],
    )
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="private_caucuses", blank=True
    )
    summary = models.TextField(blank=True)
    is_confidential = models.BooleanField(default=True)
