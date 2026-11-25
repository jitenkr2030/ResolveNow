"""Documents views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.http import HttpResponseForbidden, JsonResponse, Http404


def build_page_context(request, app_name, view_name):
    """Shared context for feature pages."""
    return {
        "request": request,
        "current_app": app_name,
        "current_view": view_name,
        "feature_title": view_name.replace("_", " ").title(),
    }


@login_required
def document_list(request, *args, **kwargs):
    """View: document_list."""
    context = build_page_context(request, "documents", "document_list")
    context["page_title"] = "Document List"
    try:
        return render(request, "documents/list.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def dispute_documents(request, *args, **kwargs):
    """View: dispute_documents."""
    context = build_page_context(request, "documents", "dispute_documents")
    context["page_title"] = "Dispute Documents"
    try:
        return render(request, "documents/dispute_documents.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def document_upload(request, *args, **kwargs):
    """View: document_upload."""
    context = build_page_context(request, "documents", "document_upload")
    context["page_title"] = "Document Upload"
    try:
        return render(request, "documents/upload.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def document_detail(request, *args, **kwargs):
    """View: document_detail."""
    context = build_page_context(request, "documents", "document_detail")
    context["page_title"] = "Document Detail"
    try:
        return render(request, "documents/detail.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def document_download(request, *args, **kwargs):
    """View: document_download."""
    context = build_page_context(request, "documents", "document_download")
    context["page_title"] = "Document Download"
    try:
        return render(request, "documents/download.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def document_preview(request, *args, **kwargs):
    """View: document_preview."""
    context = build_page_context(request, "documents", "document_preview")
    context["page_title"] = "Document Preview"
    try:
        return render(request, "documents/preview.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def document_replace(request, *args, **kwargs):
    """View: document_replace."""
    context = build_page_context(request, "documents", "document_replace")
    context["page_title"] = "Document Replace"
    try:
        return render(request, "documents/replace.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def document_share(request, *args, **kwargs):
    """View: document_share."""
    context = build_page_context(request, "documents", "document_share")
    context["page_title"] = "Document Share"
    try:
        return render(request, "documents/share.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def document_delete(request, *args, **kwargs):
    """View: document_delete."""
    context = build_page_context(request, "documents", "document_delete")
    context["page_title"] = "Document Delete"
    try:
        return render(request, "documents/delete.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def document_versions(request, *args, **kwargs):
    """View: document_versions."""
    context = build_page_context(request, "documents", "document_versions")
    context["page_title"] = "Document Versions"
    try:
        return render(request, "documents/versions.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def document_folders(request, *args, **kwargs):
    """View: document_folders."""
    context = build_page_context(request, "documents", "document_folders")
    context["page_title"] = "Document Folders"
    try:
        return render(request, "documents/folders.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

@login_required
def folder_create(request, *args, **kwargs):
    """View: folder_create."""
    context = build_page_context(request, "documents", "folder_create")
    context["page_title"] = "Folder Create"
    try:
        return render(request, "documents/folder_create.html", context)
    except Exception:
        # Fallback to generic feature page
        return render(request, "shared/feature_page.html", context)

