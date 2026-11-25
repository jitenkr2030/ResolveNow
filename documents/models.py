"""Documents app - Secure document management (Section 6)."""
from django.db import models
from django.conf import settings
from django.utils import timezone
import os
import uuid


def document_upload_path(instance, filename):
    """Generate a secure document storage path."""
    ext = os.path.splitext(filename)[1].lower()
    return f"dispute_docs/{instance.dispute.case_ref}/{uuid.uuid4().hex}{ext}"


class Document(models.Model):
    """Secure document management (Section 6).

    Upload PDF, DOCX, XLSX, images. Categorize, share with selected
    parties, version history, access logs, expiry controls.
    """

    class Category(models.TextChoices):
        CONTRACT = "contract", "Contract / Agreement"
        INVOICE = "invoice", "Invoice / Bill"
        CORRESPONDENCE = "correspondence", "Correspondence"
        EVIDENCE = "evidence", "Supporting Evidence"
        IDENTITY = "identity", "Identity Document"
        LEGAL = "legal", "Legal Document"
        FINANCIAL = "financial", "Financial Record"
        PHOTO = "photo", "Photograph"
        STATEMENT = "statement", "Position Statement"
        SETTLEMENT = "settlement", "Settlement Document"
        OTHER = "other", "Other"

    class Visibility(models.TextChoices):
        PRIVATE = "private", "Private - Owner Only"
        ALL_PARTIES = "all_parties", "All Parties"
        SELECTED_PARTIES = "selected_parties", "Selected Parties"
        MEDIATOR = "mediator", "Mediator & Case Manager"
        ADMIN = "admin", "Administrators"

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="documents"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=30, choices=Category.choices, default=Category.EVIDENCE
    )
    file = models.FileField(upload_to=document_upload_path, max_length=500)
    file_size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=20, blank=True)
    file_hash = models.CharField(max_length=128, blank=True)
    version_number = models.PositiveIntegerField(default=1)
    parent_document = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="versions",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="uploaded_documents"
    )
    visibility = models.CharField(
        max_length=20, choices=Visibility.choices, default=Visibility.PRIVATE
    )
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="shared_documents", blank=True
    )
    is_evidence = models.BooleanField(default=False)
    is_confidential = models.BooleanField(default=False)
    authenticity_declaration = models.BooleanField(
        default=False,
        help_text="Uploader declares the document is authentic.",
    )
    expires_at = models.DateTimeField(null=True, blank=True)
    is_replaced = models.BooleanField(default=False)
    replaced_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replaces",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["dispute", "category"]),
            models.Index(fields=["uploaded_by"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.dispute.case_ref})"

    @property
    def filename(self):
        return os.path.basename(self.file.name) if self.file else ""

    @property
    def extension(self):
        return os.path.splitext(self.filename)[1].lower() if self.filename else ""


class DocumentFolder(models.Model):
    """Private document folders within a dispute."""

    dispute = models.ForeignKey(
        "disputes.Dispute", on_delete=models.CASCADE, related_name="document_folders"
    )
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="document_folders"
    )
    documents = models.ManyToManyField(Document, related_name="folders", blank=True)
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("dispute", "name", "owner")]


class DocumentAccessLog(models.Model):
    """Access and download logs for documents (Section 6)."""

    class Action(models.TextChoices):
        VIEW = "view", "View"
        DOWNLOAD = "download", "Download"
        SHARE = "share", "Share"
        DELETE = "delete", "Delete"
        REPLACE = "replace", "Replace"
        UPLOAD = "upload", "Upload"

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="access_logs"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    action = models.CharField(max_length=20, choices=Action.choices)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    metadata_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-timestamp"]
