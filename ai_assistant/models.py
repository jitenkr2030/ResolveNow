"""AI assistant app - AI Dispute Assistant, AI Settlement Drafting (Section 21)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class AIAssistantSession(models.Model):
    """AI Dispute Assistant session (Section 21)."""

    class SessionType(models.TextChoices):
        DISPUTE_SUMMARY = "dispute_summary", "Dispute Summary"
        DOCUMENT_ORGANIZATION = "document_organization", "Document Organization"
        MISSING_INFORMATION = "missing_information", "Missing Information Detection"
        NEUTRAL_CASE_SUMMARY = "neutral_case_summary", "Neutral Case Summary"
        SETTLEMENT_DRAFT = "settlement_draft", "Settlement Drafting"
        TRANSLATION = "translation", "Multilingual Translation"
        LEGAL_RESEARCH = "legal_research", "Legal Research"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="ai_sessions"
    )
    related_dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.SET_NULL, null=True, blank=True
    )
    session_type = models.CharField(
        max_length=30, choices=SessionType.choices, default=SessionType.DISPUTE_SUMMARY
    )
    input_text = models.TextField(blank=True)
    output_text = models.TextField(blank=True)
    model_used = models.CharField(max_length=80, default="resolvenow-llm-v1")
    is_human_reviewed = models.BooleanField(default=False)
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ai_reviews",
    )
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]


class AISettlementDraft(models.Model):
    """AI-generated draft settlement terms (Section 21)."""

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="ai_drafts"
    )
    generated_by_session = models.ForeignKey(
        AIAssistantSession, on_delete=models.SET_NULL, null=True, blank=True
    )
    draft_text = models.TextField()
    proposed_terms = models.JSONField(default=list)
    proposed_payment_schedule = models.JSONField(default=list, blank=True)
    is_adopted_by_mediator = models.BooleanField(default=False)
    is_adopted_in_proposal = models.BooleanField(default=False)
    linked_settlement = models.ForeignKey(
        "settlements.SettlementRecord", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)


class TranslationJob(models.Model):
    """Multilingual mediation translation jobs (Section 21)."""

    source_language = models.CharField(max_length=30)
    target_language = models.CharField(max_length=30)
    source_text = models.TextField()
    translated_text = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    related_dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_human_verified = models.BooleanField(default=False)
    translator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="translations_done",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("translating", "Translating"),
            ("needs_review", "Needs Review"),
            ("completed", "Completed"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
